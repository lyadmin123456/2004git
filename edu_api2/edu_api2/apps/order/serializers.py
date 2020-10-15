from datetime import datetime

from rest_framework import serializers

from edu_api2.apps.course.models import CourseExpire, Course
from edu_api2.apps.order.models import Order, OrderDetail
from django_redis import get_redis_connection
from django.db import transaction


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_number", "pay_type")

        extra_kwargs = {
            "id": {"read_only": True},
            "order_number": {"read_only": True},
            "pay_type": {"write_only": True}
        }

    # 全局验证
    def validate(self, attrs):
        pay_type = attrs.get("pay_type")
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("不支持当前支付操作！")

        return attrs

    # 重写create生成订单和详情
    def create(self, validated_data):

        redis_connection = get_redis_connection("cart")

        # context获取用户id，详情需要看源码
        user_id = self.context["request"].user.id
        # user_id = 1
        incr = redis_connection.incr("order")
        # 生成唯一订单号  当前时间的时间戳，随机字符串以及用户id  拼接而成
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % incr
        # print(order_number)
        # 生成订单
        order = Order.objects.create(
            order_title="课程在线订单",
            total_price=0,
            real_price=0,
            order_number=order_number,
            order_status=0,
            pay_type=validated_data.get("pay_type"),
            credit=0,
            coupon=0,
            order_desc="英明的抉择",
            user_id=user_id,
        )
        # 在这里开始事务
        with transaction.atomic():
            # 记录事务回退到那个地方
            rollback_id = transaction.savepoint()

            # 生成订单详情,从购物车获取所有已勾选的商品
            all_course = redis_connection.hgetall("cart_%s" % user_id)
            all_select = redis_connection.smembers("selected_%s" % user_id)

            for course_id_bys, expire_id_bys in all_course.items():
                expire_id = int(expire_id_bys)
                course_id = int(course_id_bys)
                # course_id = 1000
                # 判断商品id是否勾选
                if course_id_bys in all_select:

                    try:
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                    except Course.DoesNotExist:
                        # 课程不存在则不进行订单详情生成，已生成好的订单也不再bao'cun
                        transaction.savepoint_rollback(rollback_id)
                        return serializers.ValidationError("当前课程不存在，生成订单失败")
                    # 如果有有效期选项，计算商品价格
                    original_price = course.price
                    expire_text = "永久有效"

                    try:
                        if expire_id > 0:
                            course_expire = CourseExpire.objects.get(id=expire_id)
                            # 对应有效期的价格
                            original_price = course_expire.price
                            expire_text = course_expire.expire_text
                    except CourseExpire.DoesNotExist:
                        pass

                    # 根据勾选商品对应有效期的价格，计算勾选商品的总价
                    real_expire_price = course.real_expire_price(expire_id)

                    # 生成订单详情
                    try:
                        OrderDetail.objects.create(
                            order=order,
                            course=course,
                            expire=expire_id,
                            price=original_price,
                            real_price=real_expire_price,
                            discount_name=course.discount_name,
                        )
                    except:
                        # 事务回滚
                        transaction.savepoint_rollback(rollback_id)
                        raise serializers.ValidationError("生成订单失败！")

                    # 成功后计算订单总价
                    order.total_price += float(original_price)
                    order.real_price += float(real_expire_price)

                order.save()
                for course_select in all_select:
                    redis_connection.hdel("cart_%s" % user_id, course_select)
            return order

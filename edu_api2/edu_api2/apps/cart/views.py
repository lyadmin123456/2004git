import logging

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ViewSet

from edu_api2.apps.course.models import Course, CourseExpire

# 获取日志记录器
from edu_api2.settings import constanst

log = logging.getLogger("django")


class CartViewSet(ViewSet):
    # 加上该逻辑，只有登录且认证成功的用户才能访问
    permission_classes = [IsAuthenticated]

    # 购物车添加方法
    def add_cart(self, request):
        course_id = request.data.get("course_id")
        user_id = request.user.id  # 如果登录 就能获取到
        print(user_id)
        # 是否勾选
        select = True
        # 有效期
        expire = 0
        # 校验前端提交的参数是否正确
        try:
            Course.objects.get(is_show=True, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数不正确，请重试"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 获取redis连接对象
            redis_connection = get_redis_connection("cart")
            # 保存数据至指定库
            pipeline = redis_connection.pipeline()
            # 开启管道
            pipeline.multi()
            # 商品信息以及有效期
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 被勾选的放商品
            pipeline.sadd("selected_%s" % user_id, course_id, )
            # 开始执行
            pipeline.execute()
            # 获取所有添加进购物车的课程的数量，也就是个数，必须在提交后在获取
            course_length = redis_connection.hlen("cart_%s" % user_id)
            # print(course_length)
        # 如果报错将其放入日志中
        except:
            log.error("数据储存失败！")
            return Response({"message": "参数不正确，购物车数据添加不成功"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "商品添加成功！", "cart_length": course_length})

    # 展示购物车
    def show_cart(self, request):
        user_id = request.user.id
        print(user_id)
        redis_connection = get_redis_connection("cart")
        # print(redis_connection)
        cart_list_bys = redis_connection.hgetall("cart_%s" % user_id)
        select_list_bys = redis_connection.smembers("selected_%s" % user_id)
        # print(cart_list,111)
        # print(select_list,222)
        print(cart_list_bys, select_list_bys)
        # 做循环找出商品信息
        data = []
        for course_id_bys, expire_id_bys in cart_list_bys.items():
            expire_id = int(expire_id_bys)
            course_id = int(course_id_bys)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            # 将所需要的信息返回
            data.append({
                "selected": True if course_id_bys in select_list_bys else False,
                "course_img": constanst.IMAGE_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_id": expire_id,
                # "price": course.price,
                # 购物车列表的有效期
                "expire_list": course.expire_list,
                # 真实价格
                "real_price": course.real_expire_price(expire_id),

            })
        return Response(data)

    # 切换购物车商品状态
    def change_select(self, request):

        user_id = request.user.id
        # print(user_id)
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "当前商品不存在！"}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection("cart")
        if selected:
            # 如果selected有值，将商品添加进set中
            redis_connection.sadd("selected_%s" % user_id, course_id)
        else:
            redis_connection.srem("selected_%s" % user_id, course_id)

        return Response({"message": "状态切换成功！"})

    # 切换有效期是，展示状态
    def change_expire(self, request):

        user_id = request.user.id
        expire_id = request.data.get("expire_id")
        course_id = request.data.get("course_id")
        print(course_id, expire_id)

        try:
            course = Course.objects.get(is_show=True, is_delete=False, id=course_id)
            # 前端传过来的有效期文本id，如果存在，则修改有效期文本
            if expire_id > 0:
                expire_iem = CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)
                if not expire_iem:
                    raise Course.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "选择的课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        connection = get_redis_connection("cart")
        connection.hset("cart_%s" % user_id, course_id, expire_id)

        # 重新计算切换有效期后的价钱
        real_price = course.real_expire_price(expire_id)

        return Response({"message": "有效期切换成功！！", "real_price": real_price})

    # 获取购物车已勾选的商品
    def get_select_course(self, request):
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")
        # 获取购物车所有商品
        all_course = redis_connection.hgetall("cart_%s" % user_id)
        all_select = redis_connection.smembers("selected_%s" % user_id)
        # 商品总价
        total_price = 0
        data = []
        for course_id_bys, expire_id_bys in all_course.items():
            expire_id = int(expire_id_bys)
            course_id = int(course_id_bys)

            # 判断商品id是否勾选
            if course_id_bys in all_select:

                try:
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue
                # 如果有有效期选项，计算商品价格
                original_price=course.price
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
            # 将所需要的信息返回
                data.append({
                    "course_img": constanst.IMAGE_SRC + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    # 购物车列表的有效期
                    "expire_text":expire_text,
                    #原价
                    "price" : original_price,
                    # 计算过后的真实价格
                    "real_price": "%2.f" % float(real_expire_price),
                    #活动名称
                    "discount_name":course.discount_name
                })
                #所有商品的价格
                total_price = total_price+float(real_expire_price)
        return Response({"course_list":data,"total_price":total_price})

    # 删除购物车中的商品
    # def del_cart(self,request):
    #     user_id = request.user.id
    #     course_id = request.data.get("course_id")
    #     print(course_id)
    #     try:
    #         course = Course.objects.get(is_show=True,is_delete=False,id = course_id)
    #     except Course.DoesNotExist:
    #         return Response({"message":"当前商品不存在，删除失败！"},status=status.HTTP_400_BAD_REQUEST)
    #
    #     redis_connection = get_redis_connection("cart")
    #     if course_id:
    #         redis_connection.srem("cart_%s" % user_id, course_id)
    #     else:
    #         return Response({"message":"当前商品不存在，删除失败！"},status=status.HTTP_400_BAD_REQUEST)


# 删除购物车中的课程
class DeleteCartAPIView(APIView):
    def delete(self, request, *args, **kwargs):
        user_id = request.user.id
        course_id = kwargs.get("id")
        print(course_id)
        try:
            course = Course.objects.get(is_show=True, is_delete=False, id=course_id)
            print(course)
        except Course.DoesNotExist:
            return Response({"message": "当前商品不存在，删除失败！"}, status=status.HTTP_400_BAD_REQUEST)
        redis_connection = get_redis_connection("cart")
        if course:
            redis_connection.hdel("cart_%s" % user_id, course_id)
            # course_obj = redis_connection.smembers("selected_%s" % user_id)
            # print(course_obj)
        else:
            return Response({"message": "当前商品不存在"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "删除成功！"})
        # return Response(course_obj)
import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from edu_api2.apps.user.models import UserInfo
from edu_api2.apps.user.utils import get_user_by_account


class RegisterModelserializer(ModelSerializer):
    token = serializers.CharField(max_length=1024, read_only=True, help_text='用户token')
    msg_code = serializers.CharField(min_length=4, max_length=6, required=False, write_only=True, help_text="用户的验证码")

    class Meta:
        model = UserInfo
        fields = ("id", "username", "password", "phone", 'token', 'msg_code')
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "username": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
            "phone": {
                "write_only": True,
            },
        }

    #     验证手机号
    def validate(self, attrs):
        # 计数器
        counts = 0
        phone = attrs.get("phone")
        password = attrs.get("password")
        msg_code = attrs.get('msg_code')
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError("手机号格式错误")
            # 验证手机号是否被祖册
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None
        if user:
            raise serializers.ValidationError("当前手机号已经被注册")
        # 验证手机号短信验证码是否正确
        redis_connection = get_redis_connection('msg_code')
        phone_code = redis_connection.get("phone_%s" % phone)
        print(phone_code)
        if phone_code != msg_code:
            # 为了防止暴力破解 可以再次设置一个手机号只能验证 n次  累加
            counts += 1
            raise serializers.ValidationError("验证码不一致")

        # 成功后需要将验证码删除
        if counts >= 5:
            raise serializers.ValidationError('请求验证码次数过多')
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        hash_password = make_password(password)
        # 设置默认用户名
        username = validated_data.get('phone')
        # 添加数据

        # user = UserInfo.objects.create(phone=username, username=username, password=hash_password, )
        # from my_task.sms.tasks import send_sms
        # send_sms.delay(username, '123456')
        user = UserInfo.objects.create(phone=username, username=username, password=hash_password, )
        # 生成token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        print(user)

        return user

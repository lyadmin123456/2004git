# 自定义返回值
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from edu_api2.apps.user.models import UserInfo


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': user.username,
        "id": user.id
    }


# 多用户登录
def get_user_by_account(account):
    try:
        user = UserInfo.objects.filter(Q(username=account) | Q(phone=account)).first()
    except UserInfo.DoesNotExist:
        return None
    else:
        return user


class UserAuth(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user and user.check_password(password) and user.is_authenticated:
            return user
        else:
            return None



from rest_framework.generics import ListAPIView

from edu_api2.apps.home.constanst import BANNER_LENGTH
from edu_api2.apps.home.models import Banner, Nav
from edu_api2.apps.home.serializers import BannerModelSerializer, NavModelSerializer


# 轮播图
class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_delete=False, is_show=True).order_by("-id")[:BANNER_LENGTH]
    serializer_class = BannerModelSerializer


# 导航栏
class HeaderListAPIView(ListAPIView):
    queryset = Nav.objects.filter(is_show=True, is_delete=False).order_by("-orders")[:4]
    serializer_class = NavModelSerializer

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


from edu_api2.apps.home.models import Banner, Nav


class BannerModelSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ('img', 'link')


# 导航栏
class NavModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = ["title", "link", "is_site"]

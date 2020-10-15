from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from edu_api2.apps.order.models import Order
from edu_api2.apps.order.serializers import OrderModelSerializer


# 生成订单的视图

class OrderAPIView(CreateAPIView):
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = OrderModelSerializer

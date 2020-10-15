from django.urls import path

from edu_api2.apps.payments import views

urlpatterns = [
    path('pay/', views.AliPayAPIView.as_view(),),
    path('result/', views.AliPayResultAPIView.as_view(),)
]
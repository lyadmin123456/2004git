from django.urls import path

from edu_api2.apps.home import views

urlpatterns = [
    path('banners/', views.BannerListAPIView.as_view()),
    path("nav/", views.HeaderListAPIView.as_view()),
]

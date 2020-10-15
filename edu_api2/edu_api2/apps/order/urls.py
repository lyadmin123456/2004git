from django.urls import path

from edu_api2.apps.order import views

urlpatterns = [
    path("options/", views.OrderAPIView.as_view())
]

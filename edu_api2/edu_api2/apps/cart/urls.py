from django.urls import path

from edu_api2.apps.cart import views

urlpatterns = [
    path("options/", views.CartViewSet.as_view({"post": "add_cart",
                                                "get": "show_cart",
                                                "patch": "change_select",
                                                "put": "change_expire", })),
    path("delcart/<str:id>", views.DeleteCartAPIView.as_view()),
    path("order/", views.CartViewSet.as_view({"get": "get_select_course"}))
]

from django.urls import path

from edu_api2.apps.course import views

urlpatterns = [
    path("category/", views.CourseCategoryListAPIView.as_view()),
    path("list/", views.CourseListAPIView.as_view()),
    path("list_filter/", views.CourseFilterListAPIView.as_view()),
    path("list_filter/<str:id>", views.CourseDetialAPIView.as_view()),
    path("chapter/", views.ChapterAPIView.as_view()),
]
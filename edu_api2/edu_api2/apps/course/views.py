from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from edu_api2.apps.course.models import CourseCategory, Course, CourseChapter
from edu_api2.apps.course.pagination import CoursePageNumber
from edu_api2.apps.course.serializers import CourseCategorySerializer, CourseModelSerializer, CourseDetialSerializer, \
     ChapterModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    # 课程分类信息查询
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseCategorySerializer


class CourseListAPIView(ListAPIView):
    # 课程列表查询
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer


class CourseFilterListAPIView(ListAPIView):
    # 通过指定条件查询课程
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer

    # 根据不同的分类id查询不同的课程
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)
    # 排序
    ordering_fields = ( "students", "price")
    # 分页   只能有一个
    pagination_class = CoursePageNumber


class CourseDetialAPIView(RetrieveAPIView):
    # 课程列表查询
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseDetialSerializer

    lookup_field = 'id'


class ChapterAPIView(ListAPIView):
    #课程章节以及其对应课时的查询
    queryset = CourseChapter.objects.filter(is_show=True,is_delete=False,).order_by("orders","id")
    serializer_class = ChapterModelSerializer

    #django_filter的方法，过滤器
    filter_backends = [DjangoFilterBackend]
    #给定的过滤字段，以course来筛选，过滤，属于他自己的course
    filter_fields = ("course",)
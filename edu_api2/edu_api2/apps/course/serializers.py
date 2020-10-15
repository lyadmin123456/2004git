from rest_framework.serializers import ModelSerializer

from edu_api2.apps.course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategorySerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class CourseTeacherSerializer(ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "signature")


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    # 序列化器嵌套查询老师信息
    teacher = CourseTeacherSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list", "discount_name", "real_price"]


class TeacherSerializer(ModelSerializer):
    # 课程对应的老师的信息
    class Meta:
        model = Teacher
        fields = ("id", "name", "image", "role", "signature", "brief")


class CourseDetialSerializer(ModelSerializer):
    """课程列表"""

    # 序列化器嵌套查询老师信息
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list", "level_name", "course_video", "brief_image",
                  "discount_name", "real_price", "active_time"]


class LessonModelSerializer(ModelSerializer):
    # 章节下的每节课的序列化器
    class Meta:
        model = CourseLesson
        fields = ["id", "name", "free_trail", "duration"]


class ChapterModelSerializer(ModelSerializer):
    # 所有章节下的所有课时

    # 一对多的情况下需要指定many=True,否则不会显示详细信息，上边的老师序列化器是一对一，因此不用，一个老师对应一门课程
    coursesections = LessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ("id", "coursesections", "chapter", "name")

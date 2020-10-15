import xadmin

from edu_api2.apps.course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson, \
    CourseDiscountType, \
    CourseDiscount, Activity, CoursePriceDiscount, CourseExpire
from edu_api2.apps.user.models import UserCourse


class CourseCategoryAdmin(object):
    pass


xadmin.site.register(CourseCategory, CourseCategoryAdmin)


class CourseAdmin(object):
    pass


xadmin.site.register(Course, CourseAdmin)


class TeacherAdmin(object):
    pass


xadmin.site.register(Teacher, TeacherAdmin)


class CourseChapterAdmin(object):
    pass


xadmin.site.register(CourseChapter, CourseChapterAdmin)


class CourseLessonAdmin(object):
    pass


xadmin.site.register(CourseLesson, CourseLessonAdmin)


# '''
# 课程价格数据注册
# '''

class CourseDiscountTypeAdmin(object):
    pass


xadmin.site.register(CourseDiscountType, CourseDiscountTypeAdmin)


class CourseDiscountAdmin(object):
    pass


xadmin.site.register(CourseDiscount, CourseDiscountAdmin)


class ActivityAdmin(object):
    pass


xadmin.site.register(Activity, ActivityAdmin)


class CoursePriceDiscountAdmin(object):
    pass


xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountAdmin)


class CourseExpireAdmin(object):
    pass


xadmin.site.register(CourseExpire, CourseExpireAdmin)


# '''
# 用户购买记录
# '''
class UserCourseAdmin(object):
    pass


xadmin.site.register(UserCourse, UserCourseAdmin)

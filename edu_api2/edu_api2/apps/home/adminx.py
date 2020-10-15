import xadmin
from xadmin import views

from edu_api2.apps.home.models import Banner, Nav


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSettings)


class GlobalSetting(object):
    site_title = "百知在线教育商城后台管理系统"
    site_footer = "北京百知信息科技有限公司"
    menu_style = "accordion"


xadmin.site.register(views.CommAdminView, GlobalSetting)


# 注册banner
class BannerInfo(object):
    # 指定默认展示的列
    list_display = ["title", 'orders', "is_show"]


xadmin.site.register(Banner, BannerInfo)


# 注册导航栏
class NavInfo(object):
    # 指定默认展示的列
    list_display = ["title", 'orders', "is_show"]


xadmin.site.register(Nav, NavInfo)

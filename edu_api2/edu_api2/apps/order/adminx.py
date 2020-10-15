import xadmin

from edu_api2.apps.order import models

xadmin.site.register(models.Order)
xadmin.site.register(models.OrderDetail)

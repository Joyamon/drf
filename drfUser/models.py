from django.db import models


# Create your models here.


class Loginlogs(models.Model):
    class Meta:
        db_table = "loginlog"
        verbose_name = "登录日志"

    username = models.CharField(max_length=50, default=None)
    ip = models.CharField(max_length=50, default=None)
    login_time = models.DateTimeField(default=None)

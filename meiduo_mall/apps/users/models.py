from django.db import models

# Create your models here.

# # 1. 自定义模型
# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     mobile = models.CharField(max_length=11, unique=True)

# 2. django自带用户模型，有模型加密和密码验证
# 自定义user替换系统的user
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
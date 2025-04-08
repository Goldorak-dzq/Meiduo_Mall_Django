# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 21:21
"""
    # 用户
    from apps.users.moddel import User
    # 组
    from django.contrib.auth.models import Group
    # 权限
    from django.contrib.auth.models import Permission
"""
# 权限
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializer.permissions import PermissionModelSerializer

class PermissionModelViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionModelSerializer
    pagination_class = PageNum
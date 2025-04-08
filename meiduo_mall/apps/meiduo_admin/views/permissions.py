# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 21:21
"""
    # 用户
    from apps.users.model import User
    # 组
    from django.contrib.auth.models import Group
    # 权限
    from django.contrib.auth.models import Permission
"""
from rest_framework.response import Response
# 权限
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializer.permissions import PermissionModelSerializer, ContentTypeModelSerializer
from apps.meiduo_admin.serializer.permissions import GroupModelSerializer


class PermissionModelViewSet(ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionModelSerializer
    pagination_class = PageNum

# 权限的展示
# ContentType权限类型, 期视就是子应用对应的模型
from django.contrib.auth.models import ContentType
from rest_framework.generics import ListAPIView
class ContentTypeListAPIView(ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeModelSerializer
    pagination_class = PageNum
    def get(self, request):
        # 查询全选分类
        content = ContentType.objects.all()
        # 返回结果
        ser = ContentTypeModelSerializer(content, many=True)
        return Response(ser.data)


####################### 组管理 #####################
from django.contrib.auth.models import Group
class GroupModelViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupModelSerializer
    pagination_class = PageNum
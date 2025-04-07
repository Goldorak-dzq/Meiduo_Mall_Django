# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/6 21:41
"""
用户管理
    用户展示    获取用户信息，实现分页和搜索功能
        1.先实现用户查询
            1.1查询所有用户
            1.2将对象列表转换为满足需求的字典列表 （序列化器）
        2.实现分页
        3.实现搜岁功能
            3.1获取keyword
            3.2根据keyword进行模糊查询

    新增用户  增加一个用户
"""
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.meiduo_admin.serializer.user import UserModelSerializer
from apps.users.models import User
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from apps.meiduo_admin.utils import PageNum
class UserAPIView(ListCreateAPIView):

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword:
            # 使用Q对象实现OR逻辑查询
            return User.objects.filter(
                Q(username__contains=keyword) |
                Q(mobile__contains=keyword) |
                Q(email__contains=keyword)
            )
        return User.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = PageNum




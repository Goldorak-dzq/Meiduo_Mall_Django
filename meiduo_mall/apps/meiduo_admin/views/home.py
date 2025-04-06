# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/6 21:18

"""
日活用户
当天登录用户的总理
"""

from apps.users.models import User
from datetime import date
from rest_framework.response import Response

# 基类
from rest_framework.views import APIView
# 一般和Mixin配合使用  Mixin（增删改查）
# from rest_framework.generics import GenericAPIView
# 三级视图 以及继承了Mixin http 方法都不用写了
# from rest_framework.generics import ListAPIView, RetrieveAPIView

class DailyActiveAPIView(APIView):
    def get(self, request):
        today = date.today()
        count = User.objects.filter(last_login__gte=today).count()
        return Response({'count': count})
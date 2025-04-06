# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/5 21:53

from django.urls import path
# from rest_framework_jwt.views import obtain_jwt_token
from apps.meiduo_admin.utils import meiduo_token
from apps.meiduo_admin.views import home, user

urlpatterns = [
    path('authorizations/', meiduo_token),
    # 日活统计
    path('statistical/day_active/', home.DailyActiveAPIView.as_view()),
    # 日下单量统计
    path('statistical/day_orders/', home.DailyOrderCountAPIView.as_view()),
    # 月增用户统计
    path('statistical/month_increment/', home.MonthCountAPIView.as_view()),

    path('users/', user.UserAPIView.as_view()),

]

# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/26 11:29
from django.urls import path
from apps.users.views import UsernameCountView
urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username>/count/', UsernameCountView.as_view())
]
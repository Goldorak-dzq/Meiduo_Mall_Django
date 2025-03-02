# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/1 00:32
from django.urls import path
from apps.oauth.views import QQLoginURLView

urlpatterns = [
    path('qq/authorization/', QQLoginURLView.as_view()),

]
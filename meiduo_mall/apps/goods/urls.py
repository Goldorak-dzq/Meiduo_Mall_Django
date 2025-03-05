# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/6 01:15
from django.urls import path
from apps.goods.views import IndexView

urlpatterns = [
    path('index/', IndexView.as_view()),

]
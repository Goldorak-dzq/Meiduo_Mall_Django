# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/3 20:23
from django.urls import path
from apps.areas.views import AreaView

urlpatterns = [
    path('areas/', AreaView.as_view()),

]
# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/3 20:23
from django.urls import path
from apps.areas.views import AreaView, SubAreaView

urlpatterns = [
    path('areas/', AreaView.as_view()),
    path('areas/<id>/', SubAreaView.as_view()),

]
# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/29 01:39
from django.urls import path
from apps.carts.views import CartsView, CartsSimpleView

urlpatterns = [
    path('carts/', CartsView.as_view()),
    path('carts/simple/', CartsSimpleView.as_view()),

]
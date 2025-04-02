# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/2 21:22
from django.urls import path
from apps.payment.views import PayUrlView

urlpatterns = [
    path('payment/<order_id>/', PayUrlView.as_view()),


]
# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/3/31 18:15
from django.urls import path
from apps.orders.views import OrderSettlementView, OrderCommitView

urlpatterns = [
    path('orders/settlement/', OrderSettlementView.as_view()),
    path('orders/commit/', OrderCommitView.as_view()),

]
# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/27 00:21
from django.urls import path
from apps.verifications.views import ImageCodeView, SmsCodeView

urlpatterns = [
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<mobile>/', SmsCodeView.as_view()),
]

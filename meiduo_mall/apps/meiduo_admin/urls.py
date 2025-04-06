# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/5 21:53

from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('authorizations/', obtain_jwt_token),


]

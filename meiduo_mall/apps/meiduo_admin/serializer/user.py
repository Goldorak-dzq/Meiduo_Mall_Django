# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/6 21:46
from rest_framework import serializers
from apps.users.models import User
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'  # 偷懒
        fields = ['id', 'username', 'email', 'mobile']

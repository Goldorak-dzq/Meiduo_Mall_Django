# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 21:21
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth.models import Permission

# 权限
class PermissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
# ContentType
class ContentTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'name']

# 组
from django.contrib.auth.models import Group
class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


# 获取普通管理员
from apps.users.models import User
class AdminUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

# class AdminSaveSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'mobile', 'email', 'password']
#         extra_kwargs = {
#             'password': {
#                 'write_only': True
#             }
#         }
#         def create(self, validated_data):
#             user = super().create(validated_data)
#             user.set_password(validated_data['password'])
#             user.is_staff = True
#             user.save()
#             return user
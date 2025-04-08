# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 21:21
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth.models import Permission

class PermissionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class ContentTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['id', 'name']
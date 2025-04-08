# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 16:15
from rest_framework import serializers
from apps.goods.models import SKU

class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'

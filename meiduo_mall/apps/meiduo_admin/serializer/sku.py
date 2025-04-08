# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 16:15
from rest_framework import serializers
from apps.goods.models import SKU, SPU, GoodsCategory, SPUSpecification, SpecificationOption


class SKUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = '__all__'
# 三级分类数据数据序列化器
class GoodsCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = ['id', 'name']
# SPU
class SPUModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPU
        fields = ['id', 'name']


# SPU规格选项序列化器
class OptionsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationOption
        fields =['id', 'value']
# SPU规格序列化器
class SpecsModelSerializer(serializers.ModelSerializer):
    options = OptionsModelSerializer(many=True)
    class Meta:
        model = SPUSpecification
        fields = ['id', 'name', 'options']
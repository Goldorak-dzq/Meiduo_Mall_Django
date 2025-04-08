# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 16:15
from rest_framework import serializers
from apps.goods.models import SKU, SPU, GoodsCategory, SPUSpecification, SpecificationOption, SKUSpecification
# SKUSpecification序列化器 (SKU规格和规格选项)
class SKUSpecificationModelSerializer(serializers.ModelSerializer):
    spec_id = serializers.IntegerField()
    option_id = serializers.IntegerField()
    class Meta:
        model = SKUSpecification
        fields = ['spec_id', 'option_id']


# SKU序列化器
class SKUModelSerializer(serializers.ModelSerializer):
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    # StringRelatedField本质获取关联模型的_str_的数据
    spu = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    specs = SKUSpecificationModelSerializer(many=True)
    class Meta:
        model = SKU
        fields = '__all__'

    def create(self, validated_data):
        # 获取规格信息,并从validated_data数据中,删除规格信息数据
        specs_data = validated_data.pop('specs')
        from django.db import transaction
        with transaction.atomic():
            # 事物开始点
            save_point = transaction.savepoint()
            try:
                # 保存sku
                sku = SKU.objects.create(**validated_data)
                # 对规格信息进行遍历,来保存商品规格信息
                for spec_data in specs_data:
                    SKUSpecification.objects.create(sku=sku, **spec_data)
            except Exception:
                transaction.savepoint_rollback(save_point)
            else:
                # 事物提交
                transaction.savepoint_commit(save_point)
            # 返回sku
            return sku
    def update(self, instance, validated_data):
        # pop规格和规格选项数据
        specs = validated_data.pop('specs')
        # 更新sku数据
        super().update(instance, validated_data)
        # 更新规格和规格选项
        # 1.
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        # instance.save()
        # 2.
        for spec in specs:
            SKUSpecification.objects.filter(sku=instance, spec_id=spec.get('spec_id')).update(option_id=spec.get('option_id'))
        return instance

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
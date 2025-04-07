# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/7 14:33
from rest_framework import serializers
from apps.goods.models import SKUImage, SKU
import time
class SKUImageModelSerializer(serializers.ModelSerializer):
    # 返回图片关联的sku的id值
    sku = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.SerializerMethodField()  # 自定义字段
    class Meta:
        model = SKUImage
        fields = '__all__'
        # fields = ('sku', 'image', 'id')

    def get_image(self, obj):
        # 示例：生成带签名的 CDN 地址
        cdn_base = "http://192.168.88.111:8888"
        timestamp = int(time.time())
        return f"{cdn_base}{obj.image.url}?ts={timestamp}"

class ImageSKUModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = ['id', 'name']

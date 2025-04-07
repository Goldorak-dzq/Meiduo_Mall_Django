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

    def update(self, instance, validated_data):
        image_data = validated_data.get("image").read()
        # 创建FastDFS连接对象
        from fdfs_client.client import Fdfs_client
        client = Fdfs_client('apps/meiduo_mall/utils/fastdfs/client.conf')
        # 上传图片到fastDFS
        result = client.upload_by_buffer(image_data)
        # 判断是否上传成功
        if result['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败，请稍后再试')

        file_id = result.get('Remote file_id')
        # 更新模型的image数据
        instance.sku_id = validated_data.get("sku_id")
        instance.image = file_id
        instance.save()
        # 返回响应
        return instance

class ImageSKUModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = ['id', 'name']

# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/7 14:33
from rest_framework import serializers
import time
from apps.goods.models import SKUImage, SKU

class SKUImageModelSerializer(serializers.ModelSerializer):
    # 返回图片关联的sku的id值
    sku = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.SerializerMethodField()  # 自定义字段
    image_file = serializers.ImageField(write_only=True)  # 新增可写字段

    class Meta:
        model = SKUImage
        fields = '__all__'


    def get_image(self, obj):
        # 示例：生成带签名的 CDN 地址
        cdn_base = "http://192.168.88.111:8888"
        timestamp = int(time.time())
        return f"{cdn_base}{obj.image.url}?ts={timestamp}"

    def update(self, instance, validated_data):

        """
        1. 创建Fdfs客户端
        2. 上传图片
        3. 根据上传结果进行判断,获取新图片的file_id
        4. 更新 模型的 image数据
        """

        # 0 单独获取图片二进制
        image_data = validated_data.get('image_file').read()
        # 1. 创建Fdfs客户端
        from fdfs_client.client import Fdfs_client
        # client = Fdfs_client('utils/fastdfs/client.conf')
        from fdfs_client.client import get_tracker_conf
        tracker_conf = get_tracker_conf('utils/fastdfs/client.conf')
        client = Fdfs_client(tracker_conf)  # 传入字典格式的配置
        # 2. 上传图片
        result = client.upload_by_buffer(image_data)
        # 3. 根据上传结果进行判断,获取新图片的file_id
        if result['Status'] != 'Upload successed.':
            raise serializers.ValidationError('上传失败,请稍后再试')

        file_id=result.get('Remote file_id')
        # 4. 更新 模型的 image数据
        instance.sku_id = validated_data.get('sku')
        instance.image = file_id
        instance.save()

        return instance




class ImageSKUModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SKU
        fields = ['id', 'name']

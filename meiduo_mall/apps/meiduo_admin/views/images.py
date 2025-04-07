# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/7 14:33
from django.core.serializers import serialize
from django.db.models.expressions import result
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage
from apps.meiduo_admin.serializer.images import SKUImageModelSerializer
from apps.meiduo_admin.utils import PageNum
from rest_framework.response import Response
from rest_framework import status


class ImageModelViewSet(ModelViewSet):
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageModelSerializer
    pagination_class = PageNum

    def create(self, request, *args, **kwargs):
        # 单独接受二进制图片
        image = request.data.get('image')
        image_data = image.read()
        # 1.接受数据
        sku_id = request.data['sku']
        # 2.验证数据
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # 3.保存数据
        #     3.1创建Fdfs的客户端口
        from fdfs_client.client import Fdfs_client
        client = Fdfs_client('utils/fastdfs/client.conf')
        #     3.2 上传图片
        result = client.upload_by_buffer(image_data)
        #     3.3根据上传的结果，获取file_id
        if result['Status'] != 'Upload successed.':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file_id = result.get('Remote file_id')
        # 3.4保存SKUImage
        new_image= SKUImage.objects.create(
            sku_id=sku_id,
            image=file_id,
        )
        # 4.返回响应
        return Response(
            {
                'id': new_image.id,
                'sku': sku_id,
                'image': new_image.image.url
            },
            status=status.HTTP_201_CREATED
        )

from apps.goods.models import SKU
from rest_framework.generics import GenericAPIView
from apps.meiduo_admin.serializer.images import ImageSKUModelSerializer
from rest_framework.mixins import ListModelMixin
class ImageSKUAPIView(ListModelMixin, GenericAPIView):
    queryset = SKU.objects.all()
    serializer_class = ImageSKUModelSerializer

    def get(self, request):
        return self.list(request)



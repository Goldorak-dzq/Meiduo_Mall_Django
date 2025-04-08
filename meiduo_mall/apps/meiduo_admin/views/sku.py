# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 16:15

from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU
from apps.meiduo_admin.serializer.sku import SKUModelSerializer
from apps.meiduo_admin.utils import PageNum

class SKUModelViewSet(ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUModelSerializer
    pagination_class = PageNum

    def get_queryset(self):
        # 提取keyword
        keyword = self.request.query_params.get('keyword')

        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(name=keyword)
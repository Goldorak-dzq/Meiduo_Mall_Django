# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/8 16:15
from click import option
from django.core.serializers import serialize
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU, SPU, SPUSpecification, SpecificationOption
from apps.meiduo_admin.serializer.sku import SKUModelSerializer, GoodsCategoryModelSerializer, SpecsModelSerializer
from apps.meiduo_admin.serializer.sku import SPUModelSerializer
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


# 三级分类数据
from apps.goods.models import GoodsCategory
class GoodsCategoryAPIView(ListAPIView):
    queryset = GoodsCategory.objects.filter(subs=None)
    serializer_class = GoodsCategoryModelSerializer


# 获取所有SPU数据
class SPUListAPIView(ListAPIView):
    queryset = SPU.objects.all()
    serializer_class = SPUModelSerializer


# SPU规格和规格选项
from apps.meiduo_admin.serializer.sku import SpecsModelSerializer
from rest_framework.views import APIView
class SPUSpecAPIView(APIView):
    def get(self, request, spu_id):
        # 1.spu_id
        # 2.获取商品SPU规格
        specs = SPUSpecification.objects.filter(spu_id=spu_id)
        # 3.根据spu规格获取对应选项信息
        serializer = SpecsModelSerializer(specs, many=True)
        return Response(serializer.data)

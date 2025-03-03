from django.shortcuts import render

# Create your views here.
"""
获取省份信息

前端
   当页面加载的时候，会发生的axios请求 来获取省份信息
后端
    请求:   不需要请求参数
    业务逻辑:  查询省份信息    
    响应: 返回JSON

    路由 GET  areas/

    步骤: 
        1.查询省份信息
        2.返回信息
      
"""
from django.views import View
from apps.areas.models import Area
from django.http import JsonResponse
class AreaView(View):
    def get(self, request):
        # 1.查询省份信息
        provinces = Area.objects.filter(parent=None)
        # 查询结构集
        # 2.将对象转换为字典数据
        provinces_list = []
        for province in provinces:
            provinces_list.append({
                'id': province.id,
                'name': province.name,
            })
        # 3.返回信息
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': provinces_list})
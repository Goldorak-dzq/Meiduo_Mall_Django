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


"""
获取市区县信息

前端
   当页面修改市县的时候，会发生的axios请求 来获取下一条信息
后端
    请求:   传递省份id、市区id
    业务逻辑:  根据id查询信息 将查询结果转换为字典列表    
    响应: 返回JSON

    路由 GET  areas/id/

    步骤: 
        1.获取省份id、市区id 查询信息
        2.将对象转换为字典数据
        3.返回响应

"""
class SubAreaView(View):
    def get(self, request, id):
        # 1.获取省份id、市区id 查询信息
        # Area.objects.filter(parent_id=id)
        # Area.objects.filter(parent=id)
        up_level = Area.objects.get(id=id)  # 市
        down_level = up_level.subs.all()  # 区县
        # 2.将对象转换为字典数据
        data_list = []
        for down_level in down_level:
            data_list.append({
                'id': down_level.id,
                'name': down_level.name,
            })
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list}})
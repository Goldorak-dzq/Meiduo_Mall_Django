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
from django.core.cache import cache
class AreaView(View):
    def get(self, request):
        # 先查询缓存数据
        province_list = cache.get('province')
        if province_list is None:
            # 1.查询省份信息
            provinces = Area.objects.filter(parent=None)
            # 查询结构集
            # 2.将对象转换为字典数据
            province_list = []
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name,
                })
            # 保存缓存数据
            # cache.set(key, value ,expire)
            cache.set('province', province_list, 24 * 3600)
        # 3.返回信息
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})


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
        # 获取缓存数据
        data_list = cache.get('city:%s' % id)
        if data_list is None:
            # 1.获取省份id、市区id 查询信息
            # Area.objects.filter(parent_id=id)
            # Area.objects.filter(parent=id)
            up_level = Area.objects.get(id=id)  # 市
            down_level = up_level.subs.all()  # 区县
            # 2.将对象转换为字典数据
            data_list = []
            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name,
                })
            cache.set('city:%s' % id, data_list, 24 * 3600)
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list}})
# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/6 21:41
"""
用户管理
    用户展示    获取用户信息，实现分页和搜索功能
        1.先实现用户查询
            1.1查询所有用户
            1.2将对象列表转换为满足需求的字典列表 （序列化器）
        2.实现分页
        3.实现搜岁功能

    新增用户  增加一个用户
"""
from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.meiduo_admin.serializer.user import UserModelSerializer
from apps.users.models import User
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict
class PageNum(PageNumberPagination):
    # 开启分页 设置默认每页多少条记录
    page_size = 5
    # 每页多少条记录的key，可以通过传递的参数传递
    page_size_query_param = 'pagesize'
    # 一页中最多有多少条记录
    max_page_size = 20
    def get_paginated_response(self, data):
        # raise NotImplementedError('get_paginated_response() must be implemented.')
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('lists', data),  # 结果列表
            ('page', self.page.number),  # 第几页
            ('pages', self.page.paginator.num_pages),  # 总共几页
            ('pagesize', self.page.paginator.per_page),  # 动态  一页多少条记录
        ]))

class UserAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    pagination_class = PageNum

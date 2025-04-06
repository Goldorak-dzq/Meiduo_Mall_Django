# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/4/6 21:18

"""
日活用户
当天登录用户的总理
"""

from apps.users.models import User
from datetime import date
from rest_framework.response import Response

# 基类
from rest_framework.views import APIView
# 一般和Mixin配合使用  Mixin（增删改查）
# from rest_framework.generics import GenericAPIView
# 三级视图 以及继承了Mixin http 方法都不用写了
# from rest_framework.generics import ListAPIView, RetrieveAPIView

class DailyActiveAPIView(APIView):
    def get(self, request):
        today = date.today()
        count = User.objects.filter(last_login__gte=today).count()
        return Response({'count': count})


"""
日下单用户量统计

"""
class DailyOrderCountAPIView(APIView):

    # permission_classes = [IsAdminUser]

    def get(self,request):
        # 获取当前日期
        today = date.today()
        # 获取当日下单用户数量  orders__create_time 订单创建时间
        count = User.objects.filter(orderinfo__create_time__gte=today).count()
        return Response({"count": count})

"""
月增用户统计
"""
from datetime import timedelta
class MonthCountAPIView(APIView):

    # permission_classes = [IsAdminUser]

    def get(self,request):
        # 获取当前日期
        now_date = date.today()
        # 获取一个月前日期
        start_date = now_date - timedelta(days=30)
        # 创建空列表保存每天的用户量
        date_list = []

        for i in range(30):
            # 循环遍历获取当天日期
            index_date = start_date + timedelta(days=i)
            # 指定下一天日期
            cur_date = start_date + timedelta(days=i + 1)

            # 查询条件是大于当前日期index_date，小于明天日期的用户cur_date，得到当天用户量
            count = User.objects.filter(date_joined__gte=index_date, date_joined__lt=cur_date).count()

            date_list.append({
                'count': count,
                'date': index_date
            })

        return Response(date_list)
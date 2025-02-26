# from Scripts.odfimgimport import image
# from django.shortcuts import render
# from django.views import View

# Create your views here.

"""
判断用户名是否重复的功能
前端: 当用户输入用户名之后，失去焦点，发生一个axios(ajax)请求
后端: 
    请求: 接受用户名
    业务逻辑:  根据用户名查询数据库,result=0 没有注册，result=0 有注册
    响应: JSON
    路由:GET  /usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/
    步骤:1.接受用户名
    2.根据用户名查询数据库
    3.返回响应
"""
import re

from django.views import View
from apps.users.models import User
from django.http import JsonResponse
class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})

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
import json
from django.views import View
from apps.users.models import User
from django.http import JsonResponse
class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})

"""
注册
步骤:1. 接受请求
    2. 获取数据
    3. 验证数据
        3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        3.2 用户名满足规则，用户名不能重复
        3.3 密码满足规则
        3.4 确认密码与密码一致
        3.5 手机号满足规则，同时不能重复
        3.6 需要同意协议
    4. 数据入库
    5. 返回响应
"""
class RegisterView(View):
    def post(self, request):
        #     1. 接受请求
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        #     2. 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        # sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')
        #     3. 验证数据
        #         3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        #         3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z0-9_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        #         3.3 密码满足规则
        #         3.4 确认密码与密码一致
        #         3.5 手机号满足规则，同时不能重复
        #         3.6 需要同意协议
        #     4. 数据入库
        # user = User(username=username, password=password, mobile=mobile, sms_code=sms_code)
        # user.save()
        # User.objects.create(username=username, password=password, mobile=mobile) # 不加密
        # 密码加密
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        #     5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
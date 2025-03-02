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
        from django.contrib.auth import login
        login(request, user)
        #     5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

"""
如果需求是注册成功后即表示用户认证通过，那么此时可以在注册成功后实现状态保持 (注册成功即已登录)
如果需求是注册成功后不表示用户认证通过，那么此时不用在注册成功后实现状态保持 (注册成功，单独登录)
实现状态保持主要有两种方式:
    客户端存储信息用Cookie
    服务器存储信息用Session
"""

"""  
登录

前端:
    当用户名把用户名和密码输入完成之后，点击登录按钮，这时候前端应该发送一个axios请求
后端:
    请求:   接受数据，验证数据
    业务逻辑: 验证用户名和密码是否正确 session
    响应: 返回JSON数据 0 成功 400 失败
步骤:
    1.接受数据
    2.验证数据
    3.验证用户名和密码是否正确
    4.session
    5.判断是否记住登录
    6.返回响应
"""

class LoginView(View):
    def post(self, request):
        # 1.接受数据
        # body_bytes = request.body
        # body_str = body_bytes.decode()
        # body_dict = json.loads(body_str)
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remembered')
        # 2.验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 确定根据手机号查询还是根据用户名查询
        if re.match('^1[3-9]\d{9}$', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 3.验证用户名和密码是否正确
        # User.objects.get(username=username)
        from django.contrib.auth import authenticate, login
        # authenticate传递用户名和密码
        # 如果正确，则返回User信息
        # 如果不正确，则返回None
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        # 4.session
        login(request, user)
        # 5.判断是否记住登录
        if remembered:
            # 记住登录 2周
            request.session.set_expiry(None)
        else:
            # 不记住密码，浏览器关闭session过期
            request.session.set_expiry(0)

        # 6.返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 首页显示用户信息，添加cookie信息
        response.set_cookie('username', user.username)
        return response

"""
退出登录

前端:
    当用户名点击退出按钮之后，前端应该发送一个axios delete请求
后端:
    请求:   接受数据，验证数据
    业务逻辑: 退出
    响应: 返回JSON数据 

"""
from django.contrib.auth import logout
class LogoutView(View):
    def delete(self, request):
        logout(request)
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        # 删除cookie信息
        response.delete_cookie('username')
        return response

"""
判断用户是否登录
用户中心也必须是登录用户
LoginRequiredMixin 未登录的用户 会返回重定向 重定向并不是JSON数据
需要返回JSON数据
"""
from utils.views import LoginRequiredJsonMixin
class CenterView(LoginRequiredJsonMixin, View):
    def get(self, request):
        return JsonResponse({'code': 0, 'errmsg': 'ok'})



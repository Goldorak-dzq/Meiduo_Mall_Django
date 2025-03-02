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
from email import message

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
        allow = body_dict.get('allow')
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
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        #         3.4 确认密码与密码一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        #         3.5 手机号满足规则，同时不能重复
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        #         3.6 需要同意协议
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})
        #     4. 数据入库
        # user = User(username=username, password=password, mobile=mobile, sms_code=sms_code)
        # user.save()
        # User.objects.create(username=username, password=password, mobile=mobile) # 不加密
        # 密码加密
        # user = User.objects.create_user(username=username, password=password, mobile=mobile)
        from django.contrib.auth import login
        try:
            user = User.objects.create_user(username=username,
                                            password=password,
                                            mobile=mobile)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})
        login(request, user)
        #     5. 返回响应
        return JsonResponse({'code': 0, 'errmsg': '注册成功'})

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
        # request.user 已经登录的用户信息
        # request.user 来源于中间件
        # 系统会判断，如果是登录用户，可以获取登录用户对应的模型实例数据
        # 如果不是登录用户，request.user = AnonymousUser() 匿名用户
        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active,
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})


"""
1.保存邮件地址 2.发送一封激活邮件 3.用户激活邮件

前端:
    当用户名输入邮箱之后，前端应该发送一个axios请求
后端:
    请求:   接受数据，获取数据
    业务逻辑: 保存邮件地址，发送一封激活邮件
    响应: 返回JSON数据
    路由: PUT
    步骤:
        1.接受请求
        2.保存数据
        3.保存邮箱地址
        4.发送一封激活邮件
        5.返回响应

"""

class EmailView(LoginRequiredJsonMixin, View):
    def put(self, request):
        # 1.接受请求
        data = json.loads(request.body.decode())
        # 2.保存数据
        email = data.get('email')
        # 验证数据
        if not email:
            return JsonResponse({'code': 400, 'errmsg': '缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400, 'errmsg': 'email格式不正确'})

        # 3.保存邮箱地址
        user = request.user
        user.email = email
        user.save()

        # 4.发送一封激活邮件
        from django.core.mail import send_mail
        subject = '美多商城激活邮件'  # 主题
        message = ""      # 邮件内容
        from_email = '美多商城<dzq1780315381@163.com>'       # 发件人
        recipient_list = ['1780315381@qq.com', 'dzq1780315381@163.com']  # 收件人列表
        # 邮件的内容如果是html 使用html_message
        # 4.1 对a标签的内容进行加密处理
        from apps.users.utils import generic_email_verify_token
        token = generic_email_verify_token(request.user.id)
        # 4.2 组织我们的激活邮件
        html_message = "点击按钮激活<a href='http://www.baidu.com/?token=%s'>激活</a>"%token
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
        )
        # 5.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})

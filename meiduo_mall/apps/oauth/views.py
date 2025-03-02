from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

"""
QQ登录
    1.准备工作
    # QQ登录参数
    # 我们申请的 客户端id
    QQ_CLIENT_ID = '101474184'
    # 我们申请的 客户端秘钥
    QQ_CLIENT_SECRET = 'c6ce949e04e12ecc909ae6a8b09b637c'
    # 我们申请时添加的: 登录成功后回调的路径
    QQ_REDIRECT_URI = 'http://www.meiduo.site:8080/oauth_callback.html'

    2.根据oauth2.0 来获取code和token
    对于应用而言，需要进行两步:
    2.1.获取Authorization Code; 表面是一个链接，实则需要用户统一然后获取code
    2.2.通过Authorization Code获取Access token;

    3.通过token换取openid(openid是此网站上唯一对应用户身份的标识，
    网站可将此ID进行存储便于用户下次登录时辨识其身份，或将其与用户在网站上的原有账号进行绑定。)
    把openid和用户信息一一绑定

生成用户绑定链接->获取code->获取token->获取openid->保存openid
"""

"""
生成用户绑定链接

前端
    当用户点击QQ登录图标时候，，前端发送一个axios请求
后端
    请求:  
    业务逻辑:  调用QQLoginTool 生成跳转链接
    响应: 返回跳转链接
    {'code':0, 'qq_login_url': "http://XXX"}
    路由 GET 
    
    步骤: 
        1.生成QQLoginTool 实例对象
        2.调用对象的方法生成 跳转链接
        3.返回响应
       
"""
from django.views import View
from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall import settings

class QQLoginURLView(View):
    def get(self, request):
        # client_id = None,  appid
        # client_secret = None, appsecret
        # redirect_uri = None,  用户同意登录之后跳转的页面
        # state = None

        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                     client_secret=settings.QQ_CLIENT_SECRET,
                     redirect_uri=settings.QQ_REDIRECT_URI,
                     state='xxx')
        qq_login_url = qq.get_qq_url()
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': qq_login_url})

"""
获取code->获取token->获取openid->保存openid

前端
   用户同意登录的code 把code发送给后端
后端
    请求:   获取code
    业务逻辑:  获取code->获取token->获取openid->保存openid
            根据openid进行判断
            如果没有绑定，需要绑定
            如果有绑定，直接登录                            
    响应: 返回跳转链接
    
    路由 GET  /oauth_callback/?code=xxx
    
    步骤: 
        1.获取code
        2.通过code获取token
        3.通过token获取openid
        4.根据openid判断 
        5.如果没有绑定，需要绑定
        6.如果有绑定，直接登录  
       
"""

from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login
from apps.users.models import User
import json
class OauthQQView(View):
    def get(self, request):
        # 1.获取code
        code = request.GET.get('code')
        if code is None:
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 2.通过code获取token
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                     client_secret=settings.QQ_CLIENT_SECRET,
                     redirect_uri=settings.QQ_REDIRECT_URI,
                     state='xxx')
        # '76350B4707C29DF72B052C49A033A030'
        token = qq.get_access_token(code)
        # 3.通过token获取openid
        # 'A56E1B92FD1BDE4E6B9B03EA842E0DE7'
        openid = qq.get_open_id(token)
        # 4.根据openid判断
        try:
            qquser = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 不存在
            # 5.如果没有绑定，需要绑定
            response = JsonResponse({'code': 400, 'access_token': openid})
            return response
        else:
            # 存在
            # 6.如果有绑定，直接登录
            # 状态保持
            # 6.1 设置session
            login(request, qquser.user)
            # 6.2 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)
            return response
    def post(self, request):
        # 1.接受请求
        data = json.loads(request.body.decode())
        # 2.获取请求参数
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        openid = data.get('access_token')
        # # 需要对数据进行验证(省略)

        # 3.根据手机号进行用户信息查询
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 手机号不存在
            # 5.查询到用户手机号没有注册， 创建user信息，然后绑定
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        else:
            # 手机号存在
            # 4.查询到用户手机号注册 判断密码是否正确，密码正确可以直接保存（绑定） 用户和openid信息
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        OAuthQQUser.objects.create(user=user, openid=openid)
        # 6.完成状态保持
        login(request, user)
        # 7.返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username)
        return response



"""
绑定账号信息

前端
    当用户输入手机号，密码，短信验证码之后 发送axios请求，请求需要携带mobile,password,sms_code,access_token(openid)
后端 
    请求:   接受请求，获取请求参数
    业务逻辑:  绑定完成状态
    响应: 返回code=0 跳转到首页
    路由 POST  oauth_callback/

    步骤: 
        1.接受请求
        2.获取请求参数
        3.根据手机号进行用户信息查询
        4.查询到用户手机号注册 判断密码是否正确，密码正确可以直接保存（绑定） 用户和openid信息
        5.查询到用户手机号没有注册， 创建user信息，然后绑定
        6.完成状态保持
        7.返回响应

"""
################itsdangerous#################
# itsdangerous数据加密
# 1.导入itsdangerous
# TimedJSONWebSignatureSerializer不仅可以对数据加密还可以设置时效
from meiduo_mall.settings import SECRET_KEY
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# 2.创建类的实例对象
# secret_key 密钥
# expires_in = None 数据的过期时间（秒）
s = Serializer(secret_key=SECRET_KEY, expires_in=3600)

# 3.加密数据
token = s.dumps({'openid': "12345657890"})
# b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTc0MDkxNDk3NCwiZXhwIjoxNzQwOTE4NTc0fQ.
# eyJvcGVuaWQiOiIxMjM0NTY1Nzg5MCJ9.kIHvCAklPYwI3GhUmGGVF2lRMRej5eZubol
# VCa3NqSPwyuZ3WUItMyar3cKtKxhuk2h1AGPOdRCn55BH059WqQ'

# itsdangerous数据解密
from meiduo_mall.settings import SECRET_KEY
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
s = Serializer(secret_key=SECRET_KEY, expires_in=3600)
s.loads(token)
# {'openid': '12345657890'}

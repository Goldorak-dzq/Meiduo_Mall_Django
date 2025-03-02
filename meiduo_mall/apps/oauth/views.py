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
from django.http import JsonResponse
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
from django.http import HttpResponse, JsonResponse
from django.views import View

""" 图片验证码
前端 
    拼接url，然后给img，img发起请求
    url=
    url=http://ip:port/image_codes/uuid/
后端
    请求: 接受路由中的uuid
    业务逻辑: 生成图片验证码和图片二进制,通过redis把图片验证码保存
    响应: 返回图片二进制
    路由: GET image_codes/uuid/
    步骤: 
        1. 接受路由中的uuid
        2. 生成图片验证码和图片二进制
        3. 通过redis把图片验证码保存
        4. 返回图片二进制
"""

# Create your views here.

class ImageCodeView(View):
    def get(self, request, uuid):
        # 1.接受路由中的uuid
        # 2. 生成图片验证码和图片二进制
        from libs.captcha.captcha import captcha
        # text 是图片验证码的内容 例如： xyzz
        # image 是图片二进制
        text, image = captcha.generate_captcha()  # 花费一天解决引用问题，原因竟然是captcha拓展包的问题


        # 3. 通过redis把图片验证码保存
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # name, time , value
        redis_cli.setex(uuid, 100, text)
        # 4. 返回图片二进制
        # content_type=响应体数据类型
        # content_type 语法: 大类/小类
        # 图片: image/jpeg, image/gif, image/png
        return HttpResponse(image, content_type='image/jpeg')

""" 短信验证码
前端
    当用户输入完手机号、图片验证码之后，前端发送一个axios请求
后端
    请求:  接受请求，获取请求参数（路由有手机号，用户的图片验证码和UUID在查询字符串中）
    业务逻辑: 验证参数 验证图片验证码 生成短信验证码 保存短信验证码 发送短信验证码
    响应: 返回响应
    {'code':0, 'errmsg': 'ok}
    
    路由 GET
    
    步骤: 
        1.获取请求参数
        2.验证参数
        3.验证图片验证码
        4.生成短信验证码
        5.保存短信验证码
        6.发送短信验证码
        7.返回响应
"""

class SmsCodeView(View):
    def get(self, request, mobile):
        # 1.获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 2.验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 3.验证图片验证码
        # 3.1 链接redis
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')
        # 3.2获取redis 数据
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        # 3.3 对比
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        # 4.生成短信验证码
        from random import randint
        sms_code = '%04d'%randint(0, 9999)
        # 5.保存短信验证码
        redis_cli.setex(mobile, 300, sms_code)
        # 6.发送短信验证码
        from libs.yuntongxun.sms import CCP
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 7.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
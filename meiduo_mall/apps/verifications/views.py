from django.http import HttpResponse
from django.views import View

"""
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
        text, image = captcha.generate_captcha()


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

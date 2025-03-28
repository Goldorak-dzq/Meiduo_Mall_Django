

# Create your views here.

"""
1.
    登录用户数据保存在服务器里 mysql/redis
    未登录用户数据保存在客户端 
2. 保存哪些数据
    redis:
        user_id,sku_Id,count,selected
    cookie: sku_id,selected
3.数据组织
    redis: 
        user_id,sku_Id,count,selected
        
        hash
        user_od:
            sku_id:count
            xxx_sku_id:selected
    cookie:
        {
            sku_id:{count:xxx,selecter:xxx},
            sku_id:{count:xxx,selecter:xxx},
            sku_id:{count:xxx,selecter:xxx},
        }
4.字典 --》pickle base64编码
pickle模块是Python的标准模块，提供了对Python数据的序列化操作，可以将数据转换为bytes类型，且序列化速度快。
pickle模块使用：
    pickle.dumps()将Python数据序列化为bytes类型数据。
    pickle.loads()将bytes类型数据反序列化为python数据
    

请求
业务逻辑 数据库的增删改查
响应
"""

import json
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU

class CartsView(View):
    """
    前端:
        点击购物车之后 前端将商品id，数量 发送给后端
    后端:
        请求： 接受参数，验证参数
        业务逻辑:
            根据商品id查询数据库看商品id是否正确
            数据入库
                登录用户 存入redis
                    连接redis
                    获取用户id
                    hash
                    set
                    返回响应
                未登录用户 存入cookie
                    先有cookie字典
                    字典转化为bytes
                    bytes类型数据转换为base64编码
                    设置cookie

        响应:  返回响应
        路由:
        步骤:
            1.接受参数
            2.验证参数
            3.判断用户登录状态
            4.登录用户 保存redis
                4.1 连接redis
                4.2 操作 hash
                4.3 操作 set
                4.4 返回响应
            5.未登录用户保存cookie
                5.1 先有cookie字典
                5.2 字典转化为bytes
                5.3 bytes类型数据转换为base64编码
                5.4 设置cookie
                5.5返回响应
    """
    def post(self, request):
        # 1.接受参数
        data = json.loads(request.body)
        sku_id = data.get('sku_id')
        count = data.get('count')
        # 2.验证参数
        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '查无此商品'})
        # 类型强制转换
        try:
            count = int(count)
        except Exception:
            count = 1
        # 3.判断用户登录状态
        # user 如果是登录用户 关联User的模型数据
        # 如果不是登录用户 就是匿名用户 is_authenticated = Flase
        user = request.user
        if user.is_authenticated:
            # 4.登录用户 保存redis
            # 4.1 连接redis
            redis_cli = get_redis_connection('carts')
            # 4.2 操作 hash
            # redis_cli.hset(key, filed, value)
            redis_cli.hset('carts_%s' % user.id, sku_id, count)
            # 4.3 操作 set
            redis_cli.sadd('selected_%s' % user.id, sku_id)
            # 4.4 返回响应
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            # 5.未登录用户保存cookie
            # 5.1 先有cookie字典
            carts = {
                sku_id: {'count': count, 'selected': True},
            }
            # 5.2 字典转化为bytes
            import pickle
            carts_bytes = pickle.dumps(carts)
            # 5.3 bytes类型数据转换为base64编码
            import base64
            base64encode = base64.b64encode(carts_bytes)
            # 5.4 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            # base64encode.decode()将bytes类型转换为 str
            # 因为value是str数据
            response.set_cookie('carts', base64encode.decode(), max_age=3600 * 24 * 12)
            # 5.5返回响应
            return response
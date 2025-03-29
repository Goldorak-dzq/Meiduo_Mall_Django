

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
import base64
import pickle
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection

from apps import carts
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
            # 先读取cookie数据
            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts:
                # 对加密的数据解密
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                # 5.1 先有cookie字典
                carts = {}

            # 判断新增的商品有没有在购物车里
            if sku_id in carts:
                # 购物车中有商品id
                origin_count = carts[sku_id]['count']
                count += origin_count
                carts[sku_id]['count'] = count

            carts[sku_id] = {
                'count': count,
                'selected': True,
            }

            # 5.2 字典转化为bytes
            carts_bytes = pickle.dumps(carts)
            # 5.3 bytes类型数据转换为base64编码
            base64encode = base64.b64encode(carts_bytes)
            # 5.4 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            # base64encode.decode()将bytes类型转换为 str
            # 因为value是str数据
            response.set_cookie('carts', base64encode.decode(), max_age=3600 * 24 * 12)
            # 5.5返回响应
            return response

    """
    1.判断用户是否登录
    2.登录用户查询redis
        2.1 连接redis
        2.2 hash {sku_id:count}
        2.3 set  {sku_id}
        2.4 遍历判断

    3.未登录用户查询cookie
        3.1 读取cookie信息
        3.2 判断是否存在购物车数据
            3.2.1存在 解码     
            3.2.2不存在 初始化空字典
    4 根据商品id查询商品信息 
    5 将对象数据转换为字典数据
    6 返回响应

    """
    def get(self, request):
        # 1.判断用户是否登录
        user = request.user
        if user.is_authenticated:
            # 2.登录用户查询redis
            #     2.1 连接redis
            redis_cli = get_redis_connection('carts')
            #     2.2 hash {sku_id:count, sku_id:count,...}
            sku_id_counts = redis_cli.hgetall('carts_%s' % user.id)
            #     2.3 set  {sku_id, sku_id, ...}
            selected_ids = redis_cli.smembers('selected_%s' % user.id)
            #     2.4 将redis数据转换为和cookie一样 后续可以统一操作
            carts = {}
            for sku_id, count in sku_id_counts.items():
                carts[sku_id] = {
                    'count': count,
                    'selected': sku_id in selected_ids,
                }

        else:
            # 3.未登录用户查询cookie
            #     3.1 读取cookie信息
            cookie_carts = request.COOKIES.get('carts')
            #     3.2 判断是否存在购物车数据
            if cookie_carts is not None:
                #         3.2.1存在 解码
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                #         3.2.2不存在 初始化空字典
                carts = {}

        # 4 根据商品id查询商品信息
        sku_ids = carts.keys()
        skus = SKU.objects.filter(id__in=sku_ids)
        sku_list = []
        for sku in skus:
            # 5 将对象数据转换为字典数据
            sku_list.append({
                # 'id': sku.id,
                # 'price': sku.price,
                # 'name': sku.name,
                # 'default_image_url': sku.default_image.url,
                # 'selected': carts[sku.id]['selected'],  # 选中状态
                # 'count': carts[sku.id]['count'],  # 数量
                # 'amount': sku.price * carts[sku.id]['count'],  # 总价格
                'id': sku.id,
                'name': sku.name,
                'count': int(carts[sku.id]['count']),  # 数量
                'selected': str(carts[sku.id]['selected']),  # 将True，转'True'，方便json解析
                'default_image_url': sku.default_image.url,
                'price': str(sku.price),  # 从Decimal('10.2')中取出'10.2'，方便json解析
                'amount': str(sku.price * carts[sku.id]['count']),
            })
        # 6 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'cart_skus': sku_list})

        """
         1. 获取用户信息
         2. 接受数据
         3. 验证数据
         4. 登录用户更新redis
            4.1 连接redis
            4.2 hash
            4.3 set
            4.4 返回响应
         5. 未登录用户查询cookie
            5.1 先读取购物车数据
                有 解码数据
                没有 初始化一个空字典
            5.2 更新数据
            5.3 重新对字典进行编码和base64加密
            5.4 设置cookie
            5.5 返回响应

        """

    def put(self, request):
        # 1. 获取用户信息
        user = request.user
        # 2. 接受数据
        data = json.loads(request.body)
        sku_id = data.get('sku_id')
        count = data.get('count')
        selected = data.get('selected')
        # 3. 验证数据
        if not all([sku_id, count]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        try:
            SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此商品'})
        try:
            count = int(count)
        except Exception:
            count = 1
        if user.is_authenticated:
            # 4. 登录用户更新redis
            #    4.1 连接redis
            redis_cli = get_redis_connection('carts')
            #    4.2 hash
            redis_cli.hset('carts_%s' % user.id, sku_id, count)
            #    4.3 set
            if selected:
                redis_cli.sadd('selected_%s' % user.id, sku_id)
            else:
                redis_cli.srem('selected_%s' % user.id, sku_id)
            #    4.4 返回响应
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'carts_sku': {'count': count, 'selected': selected}})
        else:
            # 5. 未登录用户查询cookie
            #    5.1 先读取购物车数据
            cookie_carts = request.COOKIES.get('carts')
            if cookie_carts is not None:
                #        有 解码数据
                carts = pickle.loads(base64.b64decode(cookie_carts))
            else:
                #        没有 初始化一个空字典
                carts = {}
            #    5.2 更新数据
            if sku_id in carts:
                carts[sku_id] = {
                    'count': count,
                    'selected': selected
                }
            #    5.3 重新对字典进行编码和base64加密
            new_carts = base64.b64encode(pickle.dumps(carts))
            #    5.4 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok', 'carts_sku': {'count': count, 'selected': selected}})
            response.set_cookie('carts', new_carts.decode(), max_age=3600 * 24 * 7)
            #    5.5 返回响应
            return response


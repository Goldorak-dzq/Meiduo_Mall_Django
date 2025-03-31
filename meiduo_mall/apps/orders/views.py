
# Create your views here.
"""
需求:
    提交订单页面展示
前端:
    发送一个axios请求来获取地址信息和购物车中选中商品的信息
后端:
    请求:    必须是登录用户才可以访问
    业务逻辑:   地址信息，购物车中选中的商品信息
    响应:  JSON
    路由:  GET
    步骤:
        1.获取用户信息
        2.地址信息
            2.1 查询用户的地址信息
            2.2 将对象数据转换为字典数据
        3.购物车中选中商品的信息
            3.1 连接redis
            3.2 hash
            3.3 set
            3.4 重新组织一个选中的信息
            3.5 根据商品id 查询商品的具体信息
            3.6 需要将对象数据转换为字典数据

"""
from decimal import Decimal

from django.http import JsonResponse
from django.views import View
from utils.views import LoginRequiredJsonMixin
from apps.users.models import Address
from django_redis import get_redis_connection
from apps.goods.models import SKU

class OrderSettlementView(LoginRequiredJsonMixin, View):
    def get(self, request):
        # 1.获取用户信息
        user = request.user
        # 2.地址信息
        #     2.1 查询用户的地址信息
        addresses = Address.objects.filter(is_deleted=False)
        #     2.2 将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })
        # 3.购物车中选中商品的信息
        #     3.1 连接redis
        redis_cli = get_redis_connection('carts')
        pipline = redis_cli.pipeline()
        #     3.2 hash
        pipline.hgetall('carts_%s' % user.id)
        #     3.3 set
        pipline.smembers('selected_%s' % user.id)
        result = pipline.execute()
        # result = [hash结果, set结果]
        sku_id_counts = result[0]
        selected_ids = result[1]
        #     3.4 重新组织一个选中的信息
        selected_carts = {}
        for sku_id in selected_ids:
            selected_carts[int(sku_id)] = int(sku_id_counts[sku_id])

        #     3.5 根据商品id 查询商品的具体信息
        sku_list = []
        for sku_id, count in selected_carts.items():
            sku = SKU.objects.get(id=sku_id)
            #     3.6 需要将对象数据转换为字典数据
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'default_image_url': 'http://192.168.88.111:8888' + sku.default_image.url,
                'price': sku.price,
                'count': count,
            })
        # Decimal货币类型
        # 补充运费
        freight = Decimal('10.00')
        context = {
            'skus': sku_list,
            'addresses': address_list,
            'freight': freight
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'context': context})
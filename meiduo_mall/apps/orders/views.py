
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

"""
需求:
    点击提交订单,生成订单
前端:
    发送一个axios请求 携带数据 地址id 支付方式 携带用户的session信息
后端:
    请求:    接受请求 验证数据
    业务逻辑:  数据入库
    响应:  JSON
    路由:  POST
    步骤:
        1.接受请求 user, address_id, pay_method
        2.验证数据 
        order_id
        支付状态由支付方式决定
        总数量 总金额 运费
        3.数据入库  生成订单(订单基本信息表和订单商品信息表)
            3.1 先保存订单基本信息表
            3.2 再保存订单商品信息表
                    3.2.1 连接redis
                    3.2.2 获取hash
                    3.2.3 获取set
                    3.2.4 遍历选中的商品id
                        重新一个数据 这个数据是选中的商品信息 
                    3.2.5 根据选中商品的id进行查询             
                    3.2.6 判断库存是否充足
                    3.2.7 如果充足 则库存减小 储量增加
                    3.2.8 如果不充足 下单失败
                    3.2.9 累加总数量和总金额
                    3.2.10 保存订单商品信息
        4. 更新订单的总金额和总数量
        5. 将redis 中选中的商品信息移除出去            
        6.返回响应
"""
import json
from apps.orders.models import OrderInfo

class OrderCommitView(LoginRequiredJsonMixin, View):
    def post(self, request):
        user = request.user
        # 1.接受请求 user, address_id, pay_method
        data = json.loads(request.body.decode())
        address_id = data['address_id']
        pay_method = data['pay_method']
        # 2.验证数据
        if not all([address_id, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        try:
            address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '参数不正确'})
        if pay_method not in [OrderInfo.PAY_METHODS_ENUM['CASH'], OrderInfo.PAY_METHODS_ENUM['ALIPAY']]:
            return JsonResponse({'code': 400, 'errmsg': '参数不正确'})
        # order_id
        from django.utils import timezone
        from datetime import datetime
        """
        Year month day Hour Minute Second
        """
        # 生成订单编号：年月日时分秒 + 用户编号
        order_id = timezone.localtime().strftime('%Y%m%d%H%M%S') + ('%09d' % user.id)
        # 支付状态由支付方式决定
        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:  # 货到付款
            status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']  # 待发货
        else:
            status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']  # 待支付
        # 总数量 总金额 运费
        total_count = 0
        from decimal import Decimal
        total_amount = Decimal('0')  # 总金额
        freight = Decimal('10.00')
        # 3.数据入库  生成订单(订单基本信息表和订单商品信息表)
        #     3.1 先保存订单基本信息表
        OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            address=address,
            total_count=total_count,
            total_amount=total_amount,
            freight=freight,
            pay_method=pay_method,
            status=status,
        )
        #     3.2 再保存订单商品信息表
        #             3.2.1 连接redis
        #             3.2.2 获取hash
        #             3.2.3 获取set
        #             3.2.4 遍历选中的商品id
        #                 重新一个数据 这个数据是选中的商品信息
        #             3.2.5 根据选中商品的id进行查询
        #             3.2.6 判断库存是否充足
        #             3.2.7 如果充足 则库存减小 储量增加
        #             3.2.8 如果不充足 下单失败
        #             3.2.9 累加总数量和总金额
        #             3.2.10 保存订单商品信息
        # 4. 更新订单的总金额和总数量
        # 5. 将redis 中选中的商品信息移除出去
        # 6.返回响应
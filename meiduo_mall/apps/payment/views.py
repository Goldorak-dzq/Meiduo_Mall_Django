
# Create your views here.
"""
生成跳转到支付宝的链接
保存交易完成后，支付宝返回的交易流水
需求:
    当用户点击去支付按钮的时候，在后端生成一个跳转的链接
前端:
    axios请求 携带 订单id
后端:
    请求:  获取订单id
    业务逻辑:  生成支付宝链接
            读取应用私钥和支付宝公钥
            创建支付宝实例，调用支付宝的方法
            拼接链接
    响应:  
    路由:  GET
    步骤: 
        1.获取订单id
        2.验证订单id
        3.读取应用私钥和支付宝公钥
        4.创建支付宝实例
        5.调用支付宝的方法
        6.拼接链接
        7.返回响应
"""
from django.views import View
from django.http import JsonResponse
from apps.orders.models import OrderInfo
from meiduo_mall import settings
from alipay import AliPay, AliPayConfig
from utils.views import LoginRequiredJsonMixin

class PayUrlView(LoginRequiredJsonMixin, View):
    # afgjsp2242@sandbox.com
    def get(self, request, order_id):
        user = request.user
        # 1.获取订单id
        # 2.验证订单id
        try:
            order = OrderInfo.objects.get(order_id=order_id, status=OrderInfo.ORDER_STATUS_ENUM['UNPAID'], user=user)   # 待支付
        except OrderInfo.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '没有此订单'})
        # 3.读取应用私钥和支付宝公钥
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        # 4.创建支付宝实例
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,  # 默认 False
            verbose=False,  # 输出调试数据
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )
        # 5.调用支付宝的方法
        subject = "美多商城测试订单"
        # 电脑网站支付，需要跳转到：https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(order.total_amount),  # 一定要进行类型转换
            subject=subject,
            return_url=settings.ALIPAY_RETURN_URL,   # 支付成功后跳转页面
            notify_url="https://example.com/notify"  # 可选，不填则使用默认 notify url
        )
        # 6.拼接链接
        pay_url = 'https://openapi-sandbox.dl.alipaydev.com/gateway.do?' + order_string
        # 7.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'alipay_url': pay_url})


"""
前端: 
    当用户支付完成之后，会跳转到指定商品页面
    页面中的请求 查询字符串中有 支付相关信息
    前端把这些数据提交给厚度按
后端:
    请求:  接受数据
    业务逻辑:  查询字符串转换为字典 验证数据 数据没有问题获取支付宝交易流水号
            改变订单状态
    响应:  
    路由:  PUT
    步骤: 
        1.接受数据
        2.查询字符串转换为字典
        3.验证数据
        4.改变订单状态
        5.返回响应
"""
from apps.payment.models import Payment
class PaymentStatusView(LoginRequiredJsonMixin, View):
    def put(self, request):
        # 1.接受数据
        data = request.GET
        # 2.查询字符串转换为字典
        data = data.dict()
        # 3.验证数据
        signature = data.pop('sign')
        app_private_key_string = open(settings.APP_PRIVATE_KEY_PATH).read()
        alipay_public_key_string = open(settings.ALIPAY_PUBLIC_KEY_PATH).read()
        # 4.创建支付宝实例
        alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=None,  # 默认回调 url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=settings.ALIPAY_DEBUG,  # 默认 False
            verbose=False,  # 输出调试数据
            config=AliPayConfig(timeout=15)  # 可选，请求超时时间
        )
        success = alipay.verify(data, signature)
        if success:
            # 获取支付宝交易号
            trade_no = data.get('trade_no')
            order_id = data.get('out_trade_no')
            Payment.objects.create(
                trade_id=trade_no,
                order_id=order_id,
            )
            # 4.改变订单状态
            OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM['UNSEND'])  # 未发货
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'trade_id': trade_no})
        else:
            # 5.返回响应
            return JsonResponse({'code': 400, 'errmsg': '请到个人中心的订单中查询订单状态'})
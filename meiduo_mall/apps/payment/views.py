
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

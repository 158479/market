import os
import random
from datetime import datetime
from time import sleep

from alipay import AliPay
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from goods.models import GoodsSKU
from orders.models import Transport, OrderGoods, Order, Payment
from shopcart.helper import get_cart_key, json_msg
from supermarket import settings

from user.models import AddAddress, User


# 确认订单
class ReOrder(BaseVerifyView):
    def get(self, request):
        user_id = request.session.get("ID")
        # 查询收获地址
        address = AddAddress.objects.filter(user_id=user_id).order_by('-isdefault').first()
        # 查询商品
        sku_ids = request.GET.getlist("sku_ids")
        goods_skus = []
        goods_total_price = 0

        # 连接reids
        r = get_redis_connection()
        cart_key = get_cart_key(user_id)

        # 遍历商品
        for sku_id in sku_ids:
            # 获取商品
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id)
            except GoodsSKU.DoesNotExist:
                return redirect("shopcart:购物车")
            # 获取数量
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                return redirect("shopcart:购物车")
            # 保存
            goods_sku.count = count
            goods_skus.append(goods_sku)

            # 计算价格
            goods_total_price += goods_sku.price * count
        # 运输方式
        transports = Transport.objects.filter(is_delete=False).order_by('price')
        # 渲染数据
        context = {
            'address': address,
            'goods_skus': goods_skus,
            'goods_total_price': goods_total_price,
            'transports': transports,
        }
        # 合成响应
        return render(request, 'orders/tureorder.html', context=context)

    def post(self, request):
        # 接收参数
        transport_id = request.POST.get('transport')
        sku_ids = request.POST.getlist('sku_ids')
        address_id = request.POST.get('address')

        user_id = request.session.get("ID")
        user = User.objects.get(pk=user_id)

        try:
            transport_id = int(transport_id)
            address_id = int(address_id)
            sku_ids = [int(v) for v in sku_ids]
        except:
            return JsonResponse(json_msg(2, '参数错误'))

        try:
            address = AddAddress.objects.get(pk=address_id)
        except AddAddress.DoesNotExist:
            return JsonResponse(json_msg(3, "收货地址不存在!"))

        try:
            transport = Transport.objects.get(pk=transport_id)
        except Transport.DoesNotExist:
            return JsonResponse(json_msg(4, "运输方式不存在!"))

        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
        address_info = "{}{}{}-{}".format(address.hcity, address.hproper, address.harea, address.brief)
        order = Order.objects.create(
            user=user,
            order_sn=order_sn,
            transport_price=transport.price,
            transport=transport.name,
            username=address.name,
            phone=address.phone,
            address=address_info
        )

        r = get_redis_connection()
        cart_key = get_cart_key(user_id)

        goods_total_price = 0
        for sku_id in sku_ids:
            # 获取商品
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id, is_delete=False, is_on_sale=True)
            except GoodsSKU.DoesNotExist:
                return JsonResponse(json_msg(5, "商品不存在"))
            # 获取商品数量
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                return JsonResponse(json_msg(6, "购物车中数量不存在!"))
            # 判断库存
            if int(goods_sku.tock) < count:
                return JsonResponse(json_msg(7, "库存不足!"))

            # 保存数据
            order_goods = OrderGoods.objects.create(
                order=order,
                goods_sku=goods_sku,
                price=goods_sku.price,
                count=count
            )
            # 计算价格
            goods_total_price += goods_sku.price * count
            # 对相应商品数据进行操作
            goods_sku.tock = int(goods_sku.tock)
            goods_sku.tock -= count
            goods_sku.sale = int(goods_sku.sale)
            goods_sku.sale += count
            goods_sku.save()

        order_price = goods_total_price + transport.price
        order.goods_total_price = goods_total_price
        order.order_price = order_price
        order.save()

        # 清空redis中的购物车数据
        r.hdel(cart_key, *sku_ids)

        # 合成响应
        return JsonResponse(json_msg(0, "创建订单成功!", data=order_sn))


# 确认支付
class ShowOrder(BaseVerifyView):
    def get(self, request):
        # 接收参数
        user_id = request.session.get('ID')
        order_sn = request.GET.get("order_sn")
        # 订单信息
        rs = Order.objects.get(order_sn=order_sn, user_id=user_id)
        # 支付方式
        payments = Payment.objects.filter(is_delete=False).order_by('id')
        context = {
            'rs': rs,
            'payments': payments
        }
        return render(request, 'orders/order.html', context=context)

    def post(self, request):
        # 接收参数
        # 支付方式
        payment = request.POST.get('payment')
        # 订单号
        order_sn = request.POST.get('order_sn')
        user_id = request.session.get('ID')
        try:
            payment = int(payment)
        except:
            return JsonResponse(json_msg(1, '参数错误'))
        # 判断支付方式是否存在
        try:
            payment = Payment.objects.get(pk=payment)
        except Payment.DoesNotExist:
            return JsonResponse(json_msg(2, '支付方式不存在'))
        # 判断订单是否正确
        try:
            order = Order.objects.get(user_id=user_id, order_sn=order_sn, order_status=0)
        except Order.DoesNotExist:
            return JsonResponse(json_msg(3, '没有这个订单'))

        if payment.name == '支付宝':
            app_private_key_string = open(os.path.join(settings.BASE_DIR, "alipay/user_private_key.txt")).read()
            alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay/alipay_public_key.txt')).read()
            # 初始化
            alipay = AliPay(
                appid="2016092400582068",
                app_notify_url=None,
                app_private_key_string=app_private_key_string,
                # 支付宝公钥
                alipay_public_key_string=alipay_public_key_string,
                sign_type="RSA2",
                debug=True
            )
            # 构造地址
            order_string = alipay.api_alipay_trade_wap_pay(
                out_trade_no=order.order_sn,
                total_amount=str(order.order_price),
                subject='酱油超市支付',
                return_url="http://127.0.0.1:8001/orders/pay",
                notify_url=None  # 可选, 不填则使用默认notify url
            )
            # 拼接地址
            url = "https://openapi.alipaydev.com/gateway.do?" + order_string
            return JsonResponse(json_msg(0, '创建支付地址成功', data=url))
        else:
            return JsonResponse(json_msg(4,'不支持该支付方式'))


# 支付
class Pay(BaseVerifyView):
    def get(self, request):
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "alipay/user_private_key.txt")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay/alipay_public_key.txt')).read()

        alipay = AliPay(
            appid="2016092400582068",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        order_sn = request.GET.get('out_trade_no')
        total_amount = request.GET.get('total_amount')

        paid = False
        for i in range(10):
            # 根据订单编号查询
            result = alipay.api_alipay_trade_query(out_trade_no=order_sn)
            print(result)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                # 支付成功
                paid = True
                break

            # 继续执行
            # check every 3s, and 10 times in all
            sleep(3)
            print("not paid...")

        # 判断支付是否成功
        context = {
            'order_sn': order_sn,
            'total_amount': total_amount,
        }
        if paid is False:
            # 支付失败
            context['result'] = "支付失败"
        else:
            # 支付成功
            context['result'] = "支付成功"

        return render(request, "orders/pay.html", context=context)


class Notify(View):
    def post(self, request):
        # 查询订单是否交易成功
        # 构造支付请求
        app_private_key_string = open(os.path.join(settings.BASE_DIR, "alipay/user_private_key.txt")).read()
        alipay_public_key_string = open(os.path.join(settings.BASE_DIR, 'alipay/alipay_public_key.txt')).read()

        # 初始化对象
        alipay = AliPay(
            appid="2016092400582019",
            app_notify_url=None,  # 默认回调url
            app_private_key_string=app_private_key_string,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # 获取订单编号
        order_sn = request.POST.get('out_trade_no')
        order = Order.objects.get(order_sn=order_sn)
        # check order status
        paid = False
        for i in range(10):
            # 根据订单编号查询
            result = alipay.api_alipay_trade_query(out_trade_no=order_sn)
            print(result)
            if result.get("trade_status", "") == "TRADE_SUCCESS":
                # 支付成功
                paid = True
                break

            # 继续执行
            # check every 3s, and 10 times in all
            sleep(3)
            print("not paid...")

        # 判断支付是否成功
        # 修改订单状态
        if paid is True:
            # 支付成功
            order.order_status = 1
            order.save()

        return HttpResponse("success")
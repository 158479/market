import random
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from goods.models import GoodsSKU
from orders.models import Transport, OrderGoods, Order
from shopcart.helper import get_cart_key, json_msg

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

        # 4. 清空redis中的购物车数据(对应sku_id)
        r.hdel(cart_key, *sku_ids)

        # 3. 合成响应
        return JsonResponse(json_msg(0, "创建订单成功!", data=order_sn))


# 确认支付
class ShowOrder(BaseVerifyView):
    def get(self, request):
        order_sn = request.session.get("order_sn")
        data = Order.objects.filter(order_sn=order_sn)
        context = {
            'data':data
        }
        return render(request, 'orders/order.html',context=context)

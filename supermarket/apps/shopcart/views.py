from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from goods.models import GoodsSKU
from shopcart.helper import json_msg, get_cart_count, get_cart_key


# 购物车列表
class ShopCartView(BaseVerifyView):
    def get(self, request):
        user_id = request.session.get("ID")
        # 连接redis
        r = get_redis_connection()
        cart_key = get_cart_key(user_id)
        # 获取数据
        data = r.hgetall(cart_key)
        # 创建空列表,保存商品
        goods_skus = []
        # 遍历
        for sku_id, count in data.items():
            sku_id = int(sku_id)
            count = int(count)
            # 根据id获取商品信息
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id, is_delete=False, is_on_sale=True)
            except GoodsSKU.DoesNotExist:
                r.hdel(cart_key,sku_id)
                continue

            goods_sku.count = count
            # 保存商品到商品列表
            goods_skus.append(goods_sku)
        context = {
            'goods_skus': goods_skus
        }
        return render(request, 'shopcart/shopcart.html', context=context)



# 添加购物车
class AddShopcartView(BaseVerifyView):
    def post(self, request):
        # 接收参数
        user_id = request.session.get("ID")
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")

        # 判断参数是否为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, '参数错误'))
        # 判断数据库中是否存在商品
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse(json_msg(2, '商品不存在'))
        # 商品库存是否充足
        if int(goods_sku.tock) < count:
            return JsonResponse(json_msg(3, '该商品库存不足'))
        # 连接ridis
        r = get_redis_connection()

        cart_key = get_cart_key(user_id)

        # 获取购物车已存在的数量并加上添加的数量
        g_count = r.hget(cart_key, sku_id)
        if g_count is None:
            g_count = 0
        else:
            g_count = int(g_count)

        if int(goods_sku.tock) < g_count + count:
            return JsonResponse(json_msg(3, "库存不足!"))

        # 添加到购物车
        result = r.hincrby(cart_key, sku_id, count)
        # 判断商品数量是否为0
        if result <= 0:
            r.hdel(cart_key, sku_id)

        # 获取购物车中的总数量
        cart_count = get_cart_count(request)
        # 合成响应
        return JsonResponse(json_msg(0, '添加购物车成功', data=cart_count))



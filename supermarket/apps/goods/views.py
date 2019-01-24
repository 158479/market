from django.shortcuts import render
from django.views import View

from db.base_view import BaseVerifyView

# 首页
from goods.models import GoodsSKU, Classification


class ShopView(View):
    def get(self, request):
        return render(request, 'goods/index.html')

    def post(self, request):
        pass


# 城市
class CityView(View):

    def get(self, request):
        return render(request, 'goods/city.html')

    def post(self, request):
        pass


# 校区
class SchoolView(View):
    def get(self, request):
        return render(request, 'goods/village.html')

    def post(self, request):
        pass


# 消息
class TidingsView(View):
    def get(self, request):
        return render(request, 'goods/village.html')

    def post(self, request):
        pass


# 充值
class RechargeView(View):
    def get(self, request):
        return render(request, 'goods/recharge.html')

    def post(self, request):
        pass


# 红包
class DiscountView(View):
    def get(self, request):
        return render(request, 'goods/yhq.html')

    def post(self, request):
        pass


# 零食飞速
class SpeedView(View):
    def get(self, request):
        return render(request, 'goods/speed.html')

    def post(self, request):
        pass


# 商品详情
def detail(request,id):
    goods_sku = GoodsSKU.objects.get(pk=id)
    context = {
        'goods_sku': goods_sku
    }
    return render(request, 'goods/detail.html', context=context)



class CategoryView(View):
    def get(self, request):
        categorys = Classification.objects.filter(is_delete=False)
        goods_skus = GoodsSKU.objects.filter(is_delete=False)
        context = {
            'categorys':categorys,
            'goods_skus':goods_skus
        }
        return render(request, 'goods/category.html', context=context)

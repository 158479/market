from django.shortcuts import render
from django.views import View


from goods.models import GoodsSKU, Classification
from shopcart.helper import get_cart_count

# 首页
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
class DetailView(View):
    def get(self, request, id):
        goods_sku = GoodsSKU.objects.get(pk=id)
        cart_count = get_cart_count(request)
        context = {
            'goods_sku': goods_sku,
            'cart_count':cart_count
        }
        return render(request, 'goods/detail.html', context=context)


# 商品列表
class CategoryView(View):
    def get(self, request, cate_id, order):
        # 查询所有分类
        categorys = Classification.objects.filter(is_delete=False).order_by("order")
        # 取出第一个分类
        if cate_id == "":
            category = categorys.first()
            cate_id = category.pk
        else:
            # 根据ID查询对应分类
            cate_id = int(cate_id)
            category = Classification.objects.get(pk=cate_id)

        # 查询该分类下的所有商品
        goods_skus = GoodsSKU.objects.filter(is_delete=False, classification=category)
        if order == '':
            order = 0
        order = int(order)

        # 排序
        order_rule = ['pk', '-sale', 'price', '-price', '-create_time']
        goods_skus = goods_skus.order_by(order_rule[order])

        # 获取用户购物车中的总数量
        cart_count = get_cart_count(request)

        context = {
            'categorys': categorys,
            'goods_skus': goods_skus,
            'cate_id': cate_id,
            'order': order,
            'cart_count':cart_count
        }
        return render(request, 'goods/category.html', context=context)

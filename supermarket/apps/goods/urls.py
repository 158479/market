from django.conf.urls import url

from goods.views import CityView, SchoolView, TidingsView, RechargeView, DiscountView, SpeedView, \
    CategoryView, ShopView, DetailView

urlpatterns = [
    url(r'^$', ShopView.as_view(), name='超市首页'),
    url(r'^city/$', CityView.as_view(), name='城市'),
    url(r'^school/$', SchoolView.as_view(), name='校区'),
    url(r'tidings/$', TidingsView.as_view(), name='消息中心'),
    url(r"^recharge", RechargeView.as_view(), name='充值中心'),
    url(r'^discount/$', DiscountView.as_view(), name='红包'),
    url(r'^speed/$', SpeedView.as_view(), name='零食飞速'),
    url(r'^category/(?P<cate_id>\d*)_{1}(?P<order>\d?)$', CategoryView.as_view(), name='商品列表'),
    url(r'^detail/(?P<id>\d+)$', DetailView.as_view(), name='商品详情'),
]

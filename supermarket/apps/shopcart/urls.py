from django.conf.urls import url

from shopcart.views import ShopCartView,  AddShopcartView

urlpatterns = [
    url(r'^list/$',ShopCartView.as_view(),name='购物车'),
    url(r'^add/$',AddShopcartView.as_view(),name='添加购物车'),
]
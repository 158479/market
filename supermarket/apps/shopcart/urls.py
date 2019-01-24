from django.conf.urls import url

from shopcart.views import ShopCartView

urlpatterns = [
    url(r'^shopcart/$',ShopCartView.as_view(),name='购物车')
]
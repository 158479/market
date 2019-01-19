from django.conf.urls import url

from goods.views import index, main, goods_list

urlpatterns = [
    url(r'^index/$', index, name='商品首页'),
    url(r'^main/$', main, name='商品详情'),
    url(r'^list/$', goods_list, name='商品列表')
]

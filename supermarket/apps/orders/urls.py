from django.conf.urls import url

from orders.views import ReOrder, ShowOrder, Pay

urlpatterns = [
    url(r'^reorder/$',ReOrder.as_view(),name='确认订单'),
    url(r'^order/$',ShowOrder.as_view(),name='确认支付'),
    url(r'^pay/$',Pay.as_view(),name='支付结果')
]
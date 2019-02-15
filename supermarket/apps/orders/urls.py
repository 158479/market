from django.conf.urls import url

from orders.views import ReOrder,  ShowOrder

urlpatterns = [
    url(r'^order/$',ReOrder.as_view(),name='确认订单'),
    url(r'^pay/$',ShowOrder.as_view(),name='确认支付')
]
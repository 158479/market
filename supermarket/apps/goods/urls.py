from django.conf.urls import url

from goods.views import  CityView, SchoolView, TidingsView, RechargeView, DiscountView, SpeedView, \
    CategoryView,  detail

urlpatterns = [
    url(r'^city/$',CityView.as_view(),name='城市'),
    url(r'^school/$',SchoolView.as_view(),name='校区'),
    url(r'tidings/$',TidingsView.as_view(),name='消息中心'),
    url(r"^recharge",RechargeView.as_view(),name='充值中心'),
    url(r'^discount/$',DiscountView.as_view(),name='红包'),
    url(r'^speed/$',SpeedView.as_view(),name='零食飞速'),
    url(r'^category/$',CategoryView.as_view(),name='超市'),
    url(r'^detail/(?P<id>\d+)$',detail,name='商品详情')
]

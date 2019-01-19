from django.conf.urls import url

from goods.views import main, index

urlpatterns = [
    url(r'^main/$',main,name='订单提交'),
    url(r'^index/$',index,name='订单信息')
]
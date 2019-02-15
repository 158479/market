from django.conf.urls import url

from user.views import RegisterView, LoginView, CenterView, MyInfoView, safe, RePassView, SendMailView, AddressView, \
    AddressList

urlpatterns = [
    url(r'^reg$', RegisterView.as_view(), name='注册'),
    url(r'^login$', LoginView.as_view(), name='登录'),
    url(r'^center', CenterView.as_view(), name='个人中心'),
    url(r'^myinfo', MyInfoView.as_view(), name='个人资料'),
    url(r'^safe', safe, name='安全设置'),
    url(r'^address', AddressView.as_view(), name='收货地址添加'),
    url(r'^add_list',AddressList.as_view(),name='收获地址'),
    url(r'^sendmail', SendMailView.as_view(), name='发送信息'),
    url(r'^repass', RePassView.as_view(), name='修改密码'),
]

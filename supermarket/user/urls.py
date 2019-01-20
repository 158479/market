from django.conf.urls import url

from user.views import RegisterView, LoginView, userinfo

urlpatterns = [
    url(r'^userinfo/$',userinfo,name='用户详情'),
    url(r'^reg$',RegisterView.as_view(),name='注册'),
    url(r'^login$',LoginView.as_view(),name='登录')
]
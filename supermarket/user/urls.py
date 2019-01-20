from django.conf.urls import url

from user.views import index, RegisterView, LoginView

urlpatterns = [
    url(r'^index/$',index,name='用户详情'),
    url(r'^register$',RegisterView.as_view(),name='注册'),
    url(r'^login$',LoginView.as_view(),name='登录')
]
from django.conf.urls import url

from user.views import index, login, register

urlpatterns = [
    url(r'^index/$',index,name='用户详情'),
    url(r'^login/$',login,name='用户注册'),
    url(r'^register/$',register,name='用户注册')
]
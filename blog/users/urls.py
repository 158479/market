from django.conf.urls import url

from users.views import RegisterView, LoginView

urlpatterns = [
    url(r'reg',RegisterView.as_view(),name='注册'),
    url(r'login',LoginView.as_view(),name='登录')
]
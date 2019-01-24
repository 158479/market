"""supermarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from goods.views import ShopView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user.urls', namespace='user')),
    # 上传部件自动调用的上传地址
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),
    url(r'^goods/',include('goods.urls',namespace='goods')),
    url(r'^orders/',include('orders.urls',namespace='order')),
    url(r'shopcart',include('shopcart.urls',namespace='shopcart')),
    url(r"^$",ShopView.as_view(),name='首页')
]

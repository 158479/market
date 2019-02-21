from django.utils.decorators import method_decorator
from django.views import View

from users.helper import check_login


class VerifyLoginView(View):
    """基础验证 是否登录的视图, 如果哪些视图需要登录后才能看到就继承我"""
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from db.base_view import VerifyLoginView
from users.forms import RegisterForm, LoginForm
from users.helper import set_password, login
from users.models import User


# 注册
class RegisterView(View):
    def get(self, request):
        return render(request, 'user/reg.html')

    def post(self, request):
        data = request.POST
        form = RegisterForm(data)
        if form.is_valid():
            cleaned = form.cleaned_data
            name = cleaned.get('name')
            password = set_password(cleaned.get('password'))
            data = {'name': name,
                    'password': password
                    }
            User.objects.create(**data)
            return redirect('user:登录')
        else:
            context = {
                'errors': form.errors
            }
            return render(request, 'user/reg.html', context=context)


# 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        data = request.POST
        form = LoginForm(data)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            cleaned = form.cleaned_data
            name = cleaned.get('name')
            password = set_password(cleaned.get('password'))
            try:
                User.objects.get(name=name, password=password)
                referer = request.session.get('referer')
                if referer:
                    del request.session['referer']
                    return redirect(referer)
                else:
                    return redirect('blog:博客首页'"" "")
            except:
                return render(request, 'user/login.html')
        else:  # 不合法
            context = {
                'errors': form.errors,
            }
            return render(request, "user/login.html", context=context)


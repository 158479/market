from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user import set_password
from user.forms import LoginModelForm, RegisterModelForm
from user.models import User


def userinfo(request):
    return render(request,'user/infor.html')


# 注册
class RegisterView(View):

    def get(self, request):
        return render(request, 'user/reg.html')

    def post(self, request):
        # 接收参数
        data = request.POST
        form = RegisterModelForm(data)
        # 验证判断
        if form.is_valid():
            #判断通过,保存数据并进行跳转
            cleaned_data = form.cleaned_data
            user = User()
            user.username = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            # 注册成功,跳转登录
            return redirect('user:登录')
        else:
            # 验证失败,报错,返回注册界面
            return render(request, 'user/reg.html', context={'form': form})


# 登录
class LoginView(View):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        # 接收参数
        data = request.POST
        form = LoginModelForm(data)
        if form.is_valid():
            # 根据参数进行判断,通过跳转商品列表
            user = form.cleaned_data.get('user')
            request.session['id'] = user.pk
            request.session['phone'] = user.phone
            return redirect('goods:商品首页')
        else:
            # 判断不通过,报错
            return render(request,'user/login.html',{'form':form})
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from user.forms import RegisterModelForm, LoginModelForm


def index(request):
    return render(request,'user/index.html')


# 注册
class RegisterView(View):

    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):

        # 接收参数
        data = request.POST
        form = RegisterModelForm(data)
        # 验证判断
        if form.is_valid():
            # 未创建数据库,先不填
            # cleaned_data = form.cleaned_data
            # user = User()
            # user.username = cleaned_data.get('username')
            # user.password = set_password(cleaned_data.get('password'))
            # user.save()
            # 注册成功,跳转登录
            return redirect('user:登录')
        else:
            # 验证失败,报错,返回注册界面
            return render(request, 'user/register.html', context={'form': form})


# 登录
class LoginView(View):
    def get(self,request):
        return render(request,'user/login.html')

    def post(self,request):
        # 接收参数
        data = request.POST
        form = LoginModelForm(data)
        if form.is_valid():
            # 根据参数进行判断,通过跳转首页
            user = form.cleaned_data.get('user')
            request.session['id'] = user.pk
            request.session['username'] = user.username
            return redirect('')
        else:
            # 判断不通过,报错
            return render(request,'user/login.html',{'from':form})
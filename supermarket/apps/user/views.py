import random
import re
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator

from django.views import View
from django_redis import get_redis_connection

from user import set_password
from user.forms import LoginModelForm, RegisterModelForm, MyInfoModelForm
from user.helper import check_login, login, send_sms
from user.models import User


# 个人中心
class CenterView(View):
    def get(self, request):
        return render(request, 'user/member.html', )

    def post(self, request):
        return render(request, 'user/member.html')


# 个人信息(完成)
class MyInfoView(View):
    def get(self, request):
        id = request.session.get('ID')
        data = User.objects.get(pk=id)
        context = {
            'users': data
        }
        return render(request, 'user/info.html', context=context)

    def post(self, request):
        if request.method == "POST":
            id = request.session.get('ID')
            username = request.POST.get('username')
            sex = request.POST.get('sex')
            school = request.POST.get('school')
            address = request.POST.get('address')
            hometown = request.POST.get('hometown')
            data = {
                'username' : username,
                'sex' : sex,
                'school' : school,
                'address' : address,
                'hometown' : hometown
            }
            User.objects.filter(pk=id).update(**data)
            return redirect('user:个人中心')
        else:
            return render(request, "user/info.html",)




# @method_decorator(check_login)
# def dispatch(self, request, *args, **kwargs):
#     return super().dispatch(request,*args,**kwargs)


# 注册(完成)
class RegisterView(View):
    def get(self, request):
        return render(request, 'user/reg.html')

    def post(self, request):
        # 接收参数
        data = request.POST
        form = RegisterModelForm(data)
        # 验证判断
        if form.is_valid():
            # 判断通过,保存数据并进行跳转
            cleaned_data = form.cleaned_data
            user = User()
            user.phone = cleaned_data.get('phone')
            user.password = set_password(cleaned_data.get('password'))
            user.save()
            # 注册成功,跳转登录
            return redirect('user:登录')
        else:
            # 验证失败,报错,返回注册界面
            return render(request, 'user/reg.html', {'form': form})


# 登录(完成)
class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST
        form = LoginModelForm(data)
        if form.is_valid():
            # 根据参数进行判断,通过跳转商品列表
            user = form.cleaned_data.get('user')
            # request.session['id'] = user.pk
            # request.session['phone'] = user.phone
            # request.session.set_expiry(0)
            login(request, user)
            return redirect('goods:商品首页')
        else:
            # 判断不通过,报错
            return render(request, 'user/login.html', {'form': form})


# 发送短信验证(完成)
class SendMailView(View):
    def get(self, request):
        pass

    def post(self, request):
        # 接收参数
        phone = request.POST.get('phone', '')
        # 判断电话号码是否符合格式
        result = re.search('^1[3-9]\d{9}$', phone)
        if result is None:
            return JsonResponse({'error': 1, 'errmsg': '电话格式错误'})
        # 生成验证码
        num = ''.join([str(random.randint(0, 9)) for v in range(4)])
        print(num)
        r = get_redis_connection()
        # 保存验证码
        r.set(phone, num)
        r.expire(phone, 60)
        # 获取手机号的发送次数
        key_times = '{}_times'.format(phone)
        now_times = r.get(key_times)
        if now_times is None or now_times < 5:
            r.incr(key_times)
            r.expire(key_times, 3600)
        else:
            return JsonResponse({'error': 1, 'errmsg': '发送次数过多'})
            # 导入第三方
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"打酱油的\"}" % num
        rs = send_sms(__business_id, phone, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        return JsonResponse({'error': 0})


class RePassView(View):
    def get(self, request):
        return render(request, 'user/password.html')

    def post(self, request):
        id = request.session.get('ID')
        data = request.POST
        pass
        return render(request, 'user/saftystep.html')

# 安全中心
def safe(request):
    return render(request, 'user/saftystep.html')

# 收货地址
def address(request):
    pass

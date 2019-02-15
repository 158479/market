import random
import re
import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator

from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from shopcart.helper import json_msg
from user import set_password
from user.forms import LoginModelForm, RegisterModelForm, MyInfoModelForm, AddressForm
from user.helper import check_login, login, send_sms
from user.models import User, AddAddress


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
            head = request.POST.get('head')
            if head is not None:
                User.head = head
            User.save()
            sex = request.POST.get('sex')
            school = request.POST.get('school')
            address = request.POST.get('address')
            hometown = request.POST.get('hometown')
            data = {
                'head': head,
                'username': username,
                'sex': sex,
                'school': school,
                'address': address,
                'hometown': hometown
            }
            User.objects.filter(pk=id).update(**data)
            return redirect('user:个人中心')
        else:
            return render(request, "user/info.html", )


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
            referer = request.session.get('referer')
            if referer:
                # 跳转回去
                # 删除session
                del request.session['referer']
                return redirect(referer)
            else:
                # 合成响应, 跳转到个人中心
                return redirect('user:个人中心')
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


# 添加收货地址
class AddressView(BaseVerifyView):
    def get(self, request):
        return render(request, 'user/address.html')

    def post(self, request):
        # 接收参数,并转换成字典
        data = request.POST.dict()

        # 字典保存用户
        data['user_id'] = request.session.get("ID")  # form自动转换功能

        # 验证参数
        form = AddressForm(data)
        if form.is_valid():
            form.instance.user = User.objects.get(pk=data['user_id'])
            form.save()
            return JsonResponse(json_msg(0, '添加成功'))
        else:
            return JsonResponse(json_msg(1, '添加失败', data=form.errors))


# 收获地址列表
class AddressList(BaseVerifyView):
    def get(self, request):
        # 获取用户的收货地址
        user_id = request.session.get("ID")
        user_addresses = AddAddress.objects.filter(user_id=user_id, is_delete=False).order_by("-isdefault")

        # 渲染数据
        context = {
            'addresses': user_addresses
        }
        return render(request, 'user/address_list.html', context=context)

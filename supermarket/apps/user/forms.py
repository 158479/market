from django import forms
from django.core import validators
from django_redis import get_redis_connection

from user import set_password
from user.models import User, AddAddress


# 注册
class RegisterModelForm(forms.ModelForm):
    password = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码不能小于6位',
                                   'max_length': '密码不能大于16位'
                               })
    repassword = forms.CharField(max_length=16,
                                 min_length=6,
                                 error_messages={
                                     'required': '密码不能为空',
                                     'min_length': '密码不能小于6位',
                                     'max_length': '密码不能大于16位'
                                 })

    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写"
                              })

    agree = forms.BooleanField(error_messages={
        'required': '必须同意用户协议'
    })

    class Meta:
        model = User
        fields = ['phone']

        error_messages = {
            'phone': {
                'required': '手机号不能为空',
                'max_length': '手机号长度不能大于11位',
                'min_length': '手机号长度不能小于11位'
            }
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        flag = User.objects.filter(phone=phone).exists()
        if flag:
            raise forms.ValidationError('手机号已注册')
        else:
            return phone

    def clean_verify_code(self):
        # 表单传入的验证码
        verify_code = self.cleaned_data.get('verify_code')
        sid_verify_code = self.data.get('sid_verify_code')
        if int(verify_code) != sid_verify_code:
            raise forms.ValidationError("验证码输入有误")
        else:
            return verify_code

    def clean(self):
        password = self.cleaned_data.get('password', '')
        repassword = self.cleaned_data.get('repassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError({'repassword': '密码不一致'})
        try:
            captcha = self.cleaned_data.get('captcha')
            phone = self.cleaned_data.get('phone', '')
            # 获取redis中的
            r = get_redis_connection()
            random_code = r.get(phone)  # 二进制, 转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({"captcha": "验证码输入错误!"})
        except:
            raise forms.ValidationError({"captcha": "验证码输入错误!"})
        return self.cleaned_data


# 登录
class LoginModelForm(forms.ModelForm):
    password = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码不能小于6位',
                                   'max_length': '密码不能大于16位'
                               })

    class Meta:
        model = User
        fields = ['phone']
        error_messages = {
            'phone': {
                'required': '手机号不能为空',
                'max_length': '手机号长度不能大于11位',
                'min_length': '手机号长度不能小于11位'
            }
        }

    def clean(self):
        phone = self.cleaned_data.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise forms.ValidationError({'phone': '手机号错误'})

        password = self.cleaned_data.get('password')
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码错误'})

        self.cleaned_data['user'] = user
        return self.cleaned_data


# 个人信息
class MyInfoModelForm(forms.ModelForm):
    username = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': '用户名不能为空',
                                   'min_length': '用户名不能小于6位',
                                   'max_length': '用户名不能大于16位'
                               })

    class Meta:
        model = User
        exclude = ['username']


class RePwdModelForm(forms.ModelForm):
    password = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': '密码不能为空',
                                   'min_length': '密码不能小于6位',
                                   'max_length': '密码不能大于16位'
                               })

    new_password = forms.CharField(max_length=16,
                                   min_length=6,
                                   error_messages={
                                       'required': '密码不能为空',
                                       'min_length': '密码不能小于6位',
                                       'max_length': '密码不能大于16位'
                                   })

    re_newpassword = forms.CharField(max_length=16,
                                     min_length=6,
                                     error_messages={
                                         'required': '密码不能为空',
                                         'min_length': '密码不能小于6位',
                                         'max_length': '密码不能大于16位'
                                     })

    class Meta:
        model = User
        fields = ['password']

    def clean(self):
        password = self.cleaned_data.get('new_password')
        repassword = self.cleaned_data.get('re_newpassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError({'repassword': '密码不一致'})
        else:
            return self.cleaned_data


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddAddress
        exclude = ['create_time', 'update_time', 'is_delete', 'user']

        error_messages = {
            'name': {
                'required': "请填写用户名！",
            },
            'phone': {
                'required': "请填写手机号码！",
            },
            'harea': {
                'required': "请填写完整地址！",
            },
        }

    def clean(self):
        # 验证如果数据库里地址已经超过6六表报错
        cleaned_data = self.cleaned_data
        count = AddAddress.objects.filter(user_id=self.data.get("user_id")).count()
        if count >= 6:
            raise forms.ValidationError({"harea": "收货地址最多只能保存6条"})
        if cleaned_data.get('isdefault'):
            AddAddress.objects.filter(user_id=self.data.get("user_id")).update(isdefault=False)

        return cleaned_data

from django import forms

from user import set_password
from user.models import User

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

    def clean_username(self):
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
        password = self.cleaned_data.get('password','')
        repassword = self.cleaned_data.get('repassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError({'repassword': '密码不一致'})
        else:
            return self.cleaned_data


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

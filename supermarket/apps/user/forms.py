from django import forms
from django.core import validators
from django.core.validators import RegexValidator
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

# 忘记密码
class ForgetForm(forms.Form):
    phone = forms.CharField(max_length=11,
                            error_messages={'required': '请填写手机号!'},
                            validators=[RegexValidator(r'^1[3-9]\d{9}$', message="手机号码格式错误!")]
                            )
    password2 = forms.CharField(max_length=20,
                                min_length=6,
                                error_messages={
                                    'required': '请填写密码!',
                                    'min_length': '请输入至少六个字符!',
                                    'max_length': '请输入小于或等于二十个字符!'
                                })
    repassword2 = forms.CharField(max_length=20,
                                  min_length=6,
                                  error_messages={
                                      'required': '这是必填选项!',
                                      'min_length': '请输入至少六个字符!',
                                      'max_length': '请输入小于或等于二十个字符!'
                                  })
    # 验证码
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写!"
                              })

    def clean(self):
        pwd = self.cleaned_data.get("password")  # 密码
        repwd = self.cleaned_data.get("repassword")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword": "两次密码不一致,请重新输入!"})
        # 返回,返回整个清洗后的数据
        return self.cleaned_data

    def clean_mobile(self):  # 验证用户名是否存在
        phone = self.cleaned_data.get('phone')
        flag = User.objects.filter(phont=phone).exists()
        if flag:
            # 存在 正确
            return phone
        else:
            raise forms.ValidationError("该手机未注册,请注册!")

# 修改密码
class PasswordForm(forms.Form):
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少六个字符!',
                                   'max_length': '请输入小于或等于二十个字符!'
                               })
    password2 = forms.CharField(max_length=20,
                                min_length=6,
                                error_messages={
                                    'required': '请填写修改密码!',
                                    'min_length': '请输入至少六个字符!',
                                    'max_length': '请输入小于或等于二十个字符!'
                                })
    repassword2 = forms.CharField(max_length=20,
                                  min_length=6,
                                  error_messages={
                                      'required': '这是必填选项!',
                                      'min_length': '请输入至少六个字符!',
                                      'max_length': '请输入小于或等于二十个字符!'
                                  })

    def clean(self):
        pwd = self.cleaned_data.get("password2")  # 密码
        repwd = self.cleaned_data.get("repassword2")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword2": "两次密码不一致,请重新输入!"})
        # 返回,返回整个清洗后的数据
        return self.cleaned_data


# 收货地址
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

from django import forms

from users.helper import set_password
from users.models import User, Comment


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=12,
                           min_length=2,
                           error_messages={'required': '请填写用户名!',
                                           'min_length': '请输入至少2个字符!',
                                           'max_length': '最多输入12个字符'
                                           },
                           )
    password = forms.CharField(max_length=16,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少6个字符!',
                                   'max_length': '最多输入16字符!'
                               })
    repassword = forms.CharField(max_length=16,
                                 min_length=6,
                                 error_messages={
                                     'required': '请填写密码!',
                                     'min_length': '请输入至少6个字符!',
                                     'max_length': '最多输入16字符!'
                                 })
    def clean(self):
        pwd = self.cleaned_data.get("password")  # 密码
        repwd = self.cleaned_data.get("repassword")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword": "两次密码不一致,请重新输入!"})

    def clean_name(self):  # 验证用户名是否重复
        name = self.cleaned_data.get('name')
        flag = User.objects.filter(name=name).exists()
        if flag:
            # 存在 错误
            raise forms.ValidationError("该用户名已注册,请直接登录!")
        else:
            return name


class LoginForm(forms.Form):
    name = forms.CharField(error_messages={
        'required': '请输入用户名!'
    },
    )
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少六个字符!',
                                   'max_length': '请输入小于或等于二十个字符!'
                               })

    def clean(self):
        # 验证用户名
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')
        # 验证手机号
        try:
            user = User.objects.get(name=name)
        except User.DoesNotExist:
            raise forms.ValidationError({'name': '用户名'})
        # 验证密码
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码填写错误'})

        # 用于session验证登录
        self.cleaned_data['user'] = user
        # 返回,返回整个清洗后的数据
        return self.cleaned_data



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'text']
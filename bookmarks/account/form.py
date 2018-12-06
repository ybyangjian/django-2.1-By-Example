__author__ = 'yangjian'
__date__ = '2018/12/5 18:45'

from django import forms
from django.contrib.auth.models import User

from account.models import Profile

class LoginForm(forms.Form):
    '''
    登录表单
    '''
    username = forms.CharField()
    # 将密码框渲染成password
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    '''
    注册表单，这是一个模型表单
    '''
    # 这是自己创建的两个密码框，不是User模型中的
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
    password2 = forms.CharField(label='重复密码',widget=forms.PasswordInput)

    class Meta:
        '''
         将模型表单中的username,first_name,email字段渲染出来
        '''
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        '''
        验证两次输入的密码是否一致，在调用is_valid()方法时执行，可以对任意字段采用clean_xxxx()方法验证
        :return:
        '''
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(r'两次密码不匹配')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    '''
    模型表单，依据User类生成，让用户输入姓，名和邮箱
    '''
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class ProfileEditForm(forms.ModelForm):
    '''
    模型表单，依据Profile类生成，可以让用户输入生日和上传一个头像
    '''
    class Meta:
        model = Profile
        fields = ('date_of_birth','photo')

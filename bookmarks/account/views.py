from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from account.form import LoginForm, UserRegistrationForm


def user_login(request):
    '''
    登录视图
    :param request:
    :return:
    '''
    if request.method == 'POST':
        # 实例化表单对象
        form = LoginForm(request.POST)
        # 验证表单数据
        if form.is_valid():
            cd = form.cleaned_data
            # 在数据库匹配，匹配成功返回User对象，失败返回None
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None:
                # 检查用户是否为活动用户
                if user.is_active:
                    # 设置登录状态
                    login(request,user)
                    return HttpResponse('认证成功')
                else:
                    return HttpResponse('该帐户已禁用')
            else:
                return HttpResponse('用户名或密码错误')

    else:
        form = LoginForm()
    return render(request,'account/login.html',{'form':form})


# 这个装饰器表示用户在登录的时候才会被执行
@login_required
def dashboard(request):
    # section参数用来追踪用户当前所在的模块
    return render(request,'account/dashboard.html',{'section':'dashboard'})


def register(request):
    '''
    注册视图
    :param request:
    :return:
    '''
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 建立新数据对象但不写入数据库
            new_user = user_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_form.cleaned_data['password'])
            # 保存User对象
            new_user.save()
            return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})

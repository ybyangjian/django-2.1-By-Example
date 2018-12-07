from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from account.form import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


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
            Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form':user_form})


@login_required
def edit(request):
    '''
    编辑个人信息
    :param request:
    :return:
    '''
    if request.method == 'POST':
        # instance用于指定表单类实例化为某个具体的数据对象,指定为request.user表示当前登录用户的那一条数据
        user_form = UserEditForm(instance=request.user,data=request.POST)
        # 表示当前用户对应Proile类中的那行数据，如果不指定instance参数，就会向数据库增加新记录
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'个人资料修改成功')
        else:
            messages.error(request,'更新你的个人资料时出错')
    else:
        # 当使用第三方登录时Profile表没有外键字段会报错，在这里进行验证
        #当用户修改字段的Get请求进来时，检测Profile表中该用户的外键是不是存在，
        # 如果不存在，就新建对应该用户的Profile对象，然后再用这个数据对象返回表单实例供填写。
        try:
            Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            Profile.objects.create(user=request.user)
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})

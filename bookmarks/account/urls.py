from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

__author__ = 'yangjian'
__date__ = '2018/12/5 18:56'

urlpatterns = [
    # path('login/',views.user_login,name='login'),

    path('',views.dashboard,name='dashboard'),

    # 这是Django自带的登录函数 如果需要重写模板需要在templates下新建registration目录下的html文件
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    # 修改密码
    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    # 重置密码
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    # 以上内置视图的URL用以下一行可以代替
    # path('',include('django.contrib.auth.urls')),
    # 注册
    path('register/',views.register,name='register'),
    # 编辑个人信息
    path('edit/',views.edit,name='edit'),

]
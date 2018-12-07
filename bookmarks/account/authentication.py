__author__ = 'yangjian'
__date__ = '2018/12/7 18:56'

from django.contrib.auth.models import User

class EmailAuthBackend:
    '''
        使用邮箱地址登录,需要在settings中添加
    '''

    def authenticate(self,request,username=None,password=None):
        '''
        邮箱登录验证
        :param request:
        :param username:
        :param password:
        :return:
        '''
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        '''
        返回一个userc对象
        :param user_id:
        :return:
        '''
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
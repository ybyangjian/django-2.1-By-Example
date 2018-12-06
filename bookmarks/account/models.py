from django.db import models
from django.conf import settings
# Create your models here.

class Profile(models.Model):
    '''
    扩展的用户信息模型
    '''
    # 当定义其他表与内置User模型的关系时使用settings.AUTH_USER_MODEL指代User模型
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null=True)
    # 使用图片文件字段 必须安装Pillow库才行
    photo = models.ImageField(upload_to='user/%Y/%m/%d',blank=True)

    def __str__(self):
        return '用户{}的配置文件'.format(settings.username)

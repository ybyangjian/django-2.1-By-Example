__author__ = 'yangjian'
__date__ = '2018/12/4 17:09'

from django.contrib.sitemaps import Sitemap
from .models import Post

'''
创建站点地图
url写在根url中
'''

class PostSitemap(Sitemap):
    # 文章更新频率
    changefreq = 'weekly'
    # 文章与站点的相关性，最大为1
    priority = 0.9

    def items(self):
        '''
        默认返回站点地图所需要的url
        :return:
        '''
        return Post.published.all()

    def lastmod(self,obj):
        '''
        接收items()返回的每一个数据对象然后返回其更新时间
        :param obj:
        :return:
        '''
        return obj.updated
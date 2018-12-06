__author__ = 'yangjian'
__date__ = '2018/12/4 17:22'
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

'''
为站点增加RSS或者Atom订阅信息
url写在blog应用中
'''
class LastestPostFeed(Feed):
    # 对应xml的<title>
    title = '我的博客'
    # 对应xml的<link>
    link = '/blog/'
    # 对应xml的<description>
    description = '博客新文章'

    def items(self):
        '''
        用于获得订阅信息要使用的数据对象，这里只取了最新发布的5篇文章
        :return:
        '''
        return Post.published.all()[:5]

    def item_title(self, item):
        '''
        返回标题
        :param item:
        :return:
        '''
        return item.title

    def item_description(self, item):
        '''
        返回正文前30个字符
        :param item:
        :return:
        '''
        return truncatewords(item.body,30)
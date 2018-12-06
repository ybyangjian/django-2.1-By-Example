from django.db.models import Count

__author__ = 'yangjian'
__date__ = '2018/12/4 16:52'

from django import template
from ..models import Post

# 用来注册自定义标签
register = template.Library()

# 装饰器注册简单标签
@register.simple_tag
def total_posts():
    '''
    自定义标签，返回已发布文章总数
    :return:
    '''
    return Post.published.count()

# 该标签用于渲染一段HTML代码
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    '''
    最新发布的文章
    :param count: 默认参数 5
    :return:
    '''
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    '''
    展示评论最多的文章
    :param count:
    :return:
    '''
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

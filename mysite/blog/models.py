from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    '''
    自定义的模型管理器，这里是要对已发布的文章进行操作
    '''
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

class Post(models.Model):
    '''
    文章模型
    '''
    STATUS_CHOICES = (('draft','草稿'),('published','发布'))
    # 文章标题
    title = models.CharField(max_length=250)
    # url短字符串,同时设置了不允许两条记录的title与发布时间相同
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    # 文章作者 这里有一个外键，一对多关系 on_delete表示删除外键关联的内容操作，这里表示删除作者时会删除关联的所有文章，最后是反向关联关系命名
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    # 文章正文部份
    body = models.TextField()
    # 文章发布时间
    publish = models.DateTimeField(default=timezone.now)
    # 创建文章的时间，自动用创建数据的时间填充
    created = models.DateTimeField(auto_now_add=True)
    # 修改文章的时间，自动用当前时间填充
    updated = models.DateTimeField(auto_now=True)
    # 文章状态
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    # 默认管理器
    objects = models.Manager()
    # 自定义管理器
    published = PublishedManager()
    # 第三方标签
    tags = TaggableManager()

    # 模型的元数据
    class Meta:
        # 在数据库查询的时候默认逆序
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # 创建规范化的url，返回文章详情的url
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])


class Comment(models.Model):
    # 评论关联的文章
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    # 评论人的用户名
    name = models.CharField(max_length=80)
    # 评论人的邮箱
    email = models.EmailField()
    # 评论内容
    body = models.TextField()
    # 评论创建时间
    created = models.DateTimeField(auto_now_add=True)
    # 评论修改时间
    updated = models.DateTimeField(auto_now=True)
    # 是否显示
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return '{}对{}的评论'.format(self.name,self.post)
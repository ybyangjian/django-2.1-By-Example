from django.contrib import admin
from .models import Post, Comment


# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''
    文章后台配置
    '''
    # 在详情页中显示
    list_display = ('title','slug','author','publish','status',)
    # 过滤器
    list_filter = ('status','created','publish','author',)
    # 搜索框
    search_fields = ('title','body')
    # 设置了slug与title的对应关系，title中的内容会自动填充在slug中
    prepopulated_fields = {'slug':('title',)}
    # 作者栏不再以列表展示，使用搜索
    raw_id_fields = ('author',)
    # 时间层级导航级
    date_hierarchy = 'publish'
    # 排序
    ordering = ('status','publish',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')
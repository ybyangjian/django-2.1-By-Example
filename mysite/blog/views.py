from django.core.mail import send_mail
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from taggit.models import Tag


from blog.forms import EmailPostForm, CommentForm, SearchForm
from .models import Post

# Create your views here.

class PostListView(ListView):
    '''
    类视图
    '''
    # 查询已发布的文章
    queryset = Post.published.all()
    # 模板变量的名称
    context_object_name = 'posts'
    # 每页显示的文章
    paginate_by = 3
    # 要渲染的模板
    template_name = 'blog/post/list.html'


def post_list(request,tag_slug=None):
    tag = None
    objects_list = Post.published.all()

    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        objects_list = objects_list.filter(tags__in=[tag])

    # 每页显示3篇文章
    paginator = Paginator(objects_list,3)
    # 获取到当前页码
    page = request.GET.get('page')
    try:
        # 要展示的数据
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page参数不是一个整数就返回第一页
        posts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出总页数就返回最后一页
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html',{'posts':posts,'page':page,'tag':tag})

def post_detail(request,year,month,day,post):
    '''
    文章详情页
    :param request:
    :param year:
    :param month:
    :param day:
    :param post:
    :return:
    '''
    post = get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,
                             publish__day=day)

    # 显示文章对应的所有能显示的评论
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # 通过表单直接创建新数据对象，但是不要保存到数据库中
            new_comment = comment_form.save(commit=False)
            # 设置外键为当前文章
            new_comment.post = post
            # 将评论写入数据库
            new_comment.save()
    else:
        comment_form = CommentForm()

    # 显示相近标签的文章列表
    # values_list方法返回指定的字段的值构成的元组，通过指定flat=True，让其结果变成一个列表比如[1, 2, 3, ...]
    post_tags_ids = post.tags.values_list('id',flat=True)
    # 获取当前相同标签的文章，并排除当前文章
    similar_tags = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # 对每个文章的标签记数，生成新的字段same_tags，按照相同标签的数量，降序排列结果，获取前4篇文章
    similar_posts = similar_tags.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    content = {}
    content['post'] = post
    content['comments'] = comments
    content['new_comment'] = new_comment
    content['comment_form'] = comment_form
    content['similar_posts'] = similar_posts
    return render(request,'blog/post/detail.html',content)

def post_share(request,post_id):
    '''
    发送邮件
    :param request:
    :param post_id:
    :return:
    '''
    # 通过id获取post对象
    post = get_object_or_404(Post,id=post_id,status='published')
    sent = False
    if request.method == "POST":
        # 提交表单
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 验证表单o数据
            cd = form.cleaned_data
            # 发送邮件
            # 获取到文章完整的url
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # 邮件标题
            subject = '{}({})推荐你阅读 "{}"'.format(cd['name'],cd['email'],post.title)
            # 邮件内容
            message = '阅读 "{}" 网址 {}\n\n{}\'s 评论:{}'.format(post.title,post_url,cd['name'],cd['comments'])
            # 发送邮件
            send_mail(subject,message,'809127232@qq.com',[cd['to']])
            # 发送成功为True
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{'post':post,'form':form,'sent':sent})


def post_search(request):
    '''
    搜索
    :param request:
    :return:
    '''
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # 设置搜索权重
            search_vector = SearchVector('title',weight='A')+SearchVector('body',weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.3).order_by('-rank')
    return render(request,'blog/post/search.html',{'query':query,'form':form,'results':results})
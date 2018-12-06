from blog.models import Comment

__author__ = 'yangjian'
__date__ = '2018/12/3 15:09'

from django import forms

class EmailPostForm(forms.Form):
    '''
    邮件表单（自定义字段）
    '''
    # 相当创建一个input text标签
    name = forms.CharField(max_length=25)
    # email标签，验证邮箱格式
    email = forms.EmailField()
    to = forms.EmailField()
    # 创建一个input textarea标签，内容可以为空
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    '''
    评论表单（根据评论模型创建）
    '''
    class Meta:
        # 评论模型
        model = Comment
        # 显示的字段
        fields = ('name','email','body',)


class SearchForm(forms.Form):
    '''
    搜索表单
    '''
    query = forms.CharField()
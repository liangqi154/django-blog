from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ArticlePostForm
from .models import ArticlePost, ArticleColumn
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from comment.models import Comment
from comment.forms import CommentForm
import markdown


# Create your views here.

def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    print("search:", search)
    print("order:", order)
    print("column:", column)
    print("tag:", tag)
    # 初始化查询集
    article_list = ArticlePost.objects.all()
    print("article_list:", article_list)
    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''
    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
    # 标签查询集
    # filter(tags__name__in=[tag])，意思是在tags字段中过滤name为tag的数据条目。赋值的字符串tag用方括号包起来。
    # Django-taggit还支持多标签的联合查询,比如：Model.objects.filter(tags__name__in=["tag1", "tag2"])
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    '''
    #column = request.GET.get('column')
    # 用户搜索逻辑
    if column:
        if search:
            if order == 'total_views':
                # 用 Q 对象进行联合搜索
                # icontains不区分大小写，对应的contains区分大小写
                article_list = ArticlePost.objects.filter(
                    Q(title__icontains=search) |
                    Q(body__icontains=search) |
                    Q(column__icontains=column)
                ).order_by('-total_views')
            else:
                article_list = ArticlePost.objects.filter(
                    Q(title__icontains=search) |
                    Q(body__icontains=search) |
                    Q(column__icontains=column)
                )
        else:
            # 将 search 参数重置为空
            search = ''
            if order == 'total_views':
                article_list = ArticlePost.objects.filter(
                    Q(column__icontains=column)
                ).order_by('-total_views')
            else:
                article_list = ArticlePost.objects.filter(
                    Q(column__icontains=column)
                )
    else:
        if search:
            if order == 'total_views':
                # 用 Q 对象进行联合搜索
                # icontains不区分大小写，对应的contains区分大小写
                article_list = ArticlePost.objects.filter(
                    Q(title__icontains=search) |
                    Q(body__icontains=search)
                ).order_by('-total_views')
            else:
                article_list = ArticlePost.objects.filter(
                    Q(title__icontains=search) |
                    Q(body__icontains=search)
                )
        else:
            # 将 search 参数重置为空
            search = ''
            if order == 'total_views':
                article_list = ArticlePost.objects.all().order_by('-total_views')
            else:
                article_list = ArticlePost.objects.all()
    '''
    '''
    # 用户搜索逻辑
    if search:
        if order == 'total_views':
            # 用 Q 对象进行联合搜索
            # icontains不区分大小写，对应的contains区分大小写
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()
    '''
    '''
    if request.GET.get('order') == 'total_views':
        article_list = ArticlePost.objects.all().order_by('-total_views')
        order = 'total_views'
    else:
        article_list = ArticlePost.objects.all()
        order = 'normal'
    '''
    # 每页显示 3 篇文章
    paginator = Paginator(article_list, 3)
    print("article_list:", article_list)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    context = {'articles': articles, 'order': order, 'search': search, 'column': column, 'tag': tag}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # filter()可以取出多个满足条件的对象，而get()只能取出1个
    # article = ArticlePost.objects.get(id=id)
    article = get_object_or_404(ArticlePost, id=id)
    comments = Comment.objects.filter(article=id)
    if request.FILES.get('avatar'):
        article.avatar = request.FILES.get('avatar')
    # 浏览量+1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # 目录扩展
            'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)
    comment_form = CommentForm()
    context = {'article': article,
               'toc': md.toc,
               'comments': comments,
               'comment_form': comment_form,
               }
    return render(request, 'article/detail.html', context)


# 检查登录
@login_required(login_url='/userprofile/login/')
# 写文章的视图
def article_create(request):
    # 用户如果提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        print("THE files:", request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            new_article.author = User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            # 将新文章保存到数据库中
            new_article.save()
            article_post_form.save_m2m()
            # 完成后返回到文章列表
            return redirect("article:article_list")
            # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 用户如果请求数据
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        print(columns)
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'article/create.html', context)


# 检查登录
@login_required(login_url='/userprofile/login/')
# 删除文章
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权删除这篇文章。")
    article.delete()
    return redirect("article:article_list")


# 检查登录
@login_required(login_url='/userprofile/login/')
# 安全删除
def article_safe_delete(request, id):
    if request.method == "POST":
        article = ArticlePost.objects.get(id=id)
        # 过滤非作者的用户
        if request.user != article.author:
            return HttpResponse("抱歉，你无权删除这篇文章。")
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("只允许POST请求!")


# 检查登录
@login_required(login_url='/userprofile/login/')
# 更新文章
def article_update(request, id):
    """
        更新文章的视图函数
        通过POST方法提交表单，更新titile、body字段
        GET方法进入初始表单页面
        id： 文章的 id
    """
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
                print(article.column)
            else:
                article.column = None
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("内容有误，请重新填写！")
    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article,
                   'article_post_form': article_post_form,
                   'columns': columns,
                   'tags': ','.join([x for x in article.tags.names()]),
                   }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')

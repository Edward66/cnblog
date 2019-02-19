import json
import threading

from django.contrib import auth
from django.core.mail import send_mail
from django.db.models import F
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import HttpResponse, render, redirect

from blog import models
from blog.models import UserInfo
from blog.forms.regForm import RegForm
from blog.utils.slide_auth_code import pcgetcaptcha
from cnblog import settings


# 登陆
def login(request):
    if request.method == "POST":
        response = {'user': None, 'msg': None}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        user = auth.authenticate(username=user, password=pwd)

        if user:
            auth.login(request, user)
            response['user'] = user.username
        else:
            response['msg'] = '用户名或密码错误'
        return JsonResponse(response)
    return render(request, 'login.html')


# 注销
def logout(request):
    auth.logout(request)  # request.session.flush()
    return redirect(reverse('blog:login'))


# 滑动验证码
def slide_code_auth(request):
    response_str = pcgetcaptcha(request)
    return HttpResponse(response_str)


# 首页
def index(request):
    article_list = models.Article.objects.all()
    context = {
        'article_list': article_list,
    }
    return render(request, 'index.html', context=context)


# 注册页面
def register(request):
    if request.is_ajax():
        form = RegForm(request.POST)
        response = {'user': None, 'msg': None}
        if form.is_valid():
            response['user'] = form.cleaned_data.get('user')

            # 生成一条用户记录信息
            user = form.cleaned_data.get('user')
            pwd = form.cleaned_data.get('pwd')
            email = form.cleaned_data.get('email')
            avatar_obj = request.FILES.get('avatar')

            extra = {}
            if avatar_obj:
                extra['avatar'] = avatar_obj
            UserInfo.objects.create_user(
                username=user,
                password=pwd,
                email=email,
                **extra
            )


        else:
            response['msg'] = form.errors

        return JsonResponse(response)

    form = RegForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context=context)


def home_site(request, username, **kwargs):
    """
    个人站点视图函数
    :param request:
    :return:
    """

    user = UserInfo.objects.filter(username=username).first()

    # 判断用户是否存在
    if not user:
        return render(request, 'not_found.html')

    blog = user.blog

    article_list = models.Article.objects.filter(user=user)

    if kwargs:
        condition = kwargs.get('condition')
        param = kwargs.get('param')

        if condition == 'category':
            article_list = article_list.filter(category__title=param)
        elif condition == 'tag':
            article_list = article_list.filter(tags__title=param)
        else:
            year, month = param.split('-')
            article_list = article_list.filter(created_time__year=year, created_time__month=month)
    context = {
        'blog': blog,
        'article_list': article_list,
        'username': username,
        'user': user,
    }

    return render(request, 'home_site.html', context=context)


# 文章详情页
def article_detail(request, username, article_id):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog

    article_obj = models.Article.objects.filter(pk=article_id).first()

    comment_list = models.Comment.objects.filter(article_id=article_id)
    context = {
        'username': username,
        'blog': blog,
        'comment_list': comment_list,
        'article_obj': article_obj,
    }
    return render(request, 'article_detail.html', context=context)


# 点赞
def digg(request):
    article_id = request.POST.get('article_id')
    is_up = json.loads(request.POST.get('is_up'))
    user_id = request.user.pk

    obj = models.ArticleUpDown.objects.filter(user_id=user_id, article_id=article_id).first()

    response = {'status': True}
    if not obj:

        models.ArticleUpDown.objects.create(
            user_id=user_id,
            article_id=article_id,
            is_up=is_up,
        )

        article_obj = models.Article.objects.filter(pk=article_id)
        if is_up:
            article_obj.update(up_count=F('up_count') + 1)
        else:
            article_obj.update(down_count=F('down_count') + 1)
    else:
        response['status'] = False
        response['handled'] = obj.is_up

    return JsonResponse(response)


# 评论
def comment(request):
    article_id = request.POST.get("article_id")
    pid = request.POST.get('pid')
    content = request.POST.get('content')
    user_id = request.user.pk

    article_obj = models.Article.objects.filter(pk=article_id).first()

    with transaction.atomic():  # 等同于mysql里的事物操作，下面两个操作必须同时成功，只要有一个失败那么都不会执行
        comment_obj = models.Comment.objects.create(
            user_id=user_id,
            article_id=article_id,
            content=content,
            parent_comment_id=pid
        )
        models.Article.objects.filter(pk=article_id).update(comment_count=F('comment_count') + 1)

    response = {}
    response['created_time'] = comment_obj.created_time.strftime('%Y-%m%d %X')
    response['username'] = request.user.username
    response['content'] = content
    if pid:
        parent_comment = models.Comment.objects.filter(nid=pid).first()
        response['parent_comment'] = parent_comment.content
        response['parent_name'] = parent_comment.user.username

    # 发送邮件
    t = threading.Thread(target=send_mail, args=(
        f"您的文章{article_obj.title}新增了一条评论内容",
        content,
        settings.EMAIL_HOST_USER,
        [request.user.email],
    ))
    t.start()

    return JsonResponse(response)


# 评论树
def get_comment_tree(request):
    article_id = request.GET.get('article_id')

    comment_obj = list(
        models.Comment.objects.filter(article_id=article_id).order_by('pk').values('pk', 'content',
                                                                                   'parent_comment_id',
                                                                                   'user__username'
                                                                                   ))

    # In order to allow non-dict objects to be serialized set the safe parameter to False.
    return JsonResponse(comment_obj, safe=False)

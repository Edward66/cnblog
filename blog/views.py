import json
from django.contrib import auth
from django.db.models import F
from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.urls import reverse

from blog import models
from blog.models import UserInfo
from blog.forms.regForm import RegForm
from blog.utils.slide_auth_code import pcgetcaptcha


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
    context = {
        'article_obj': article_obj,
        'username': username,
        'blog': blog,
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

        aud = models.ArticleUpDown.objects.create(
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

from django.contrib import auth
from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.urls import reverse

from blog import models
from django.db.models import Count
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


def home_site(request, username):
    """
    个人站点视图函数
    :param request:
    :return:
    """

    user = UserInfo.objects.filter(username=username).first()

    # 判断用户是否存在
    if not user:
        return render(request, 'not_found.html')

    # 查询当前站点
    blog = user.blog

    # 获取当前用户或者当前站点对应的所有文章
    # 基于对象查询
    # aritlce_list = user.article_set.all()

    # 基于双下划线查询
    article_list = models.Article.objects.filter(user=user)

    # 查询当前站点的每一个分类名称以及对应的文章数
    category_list = models.Category.objects.filter(blog=blog).values('pk').annotate(
        count=Count('article__title')).values(
        'title', 'count')

    # 查询当前站点的每一个标签名称以及对应的文章数
    tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(count=Count('article')).values_list(
        'title', 'count'
    )

    # 查询当前站点的每一个年月名称以及对应的文章数

    return render(request, 'home_site.html')

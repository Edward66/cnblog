from django.shortcuts import render

from blog import models
from blog.models import UserInfo


# 首页
def index(request):
    article_list = models.Article.objects.all()
    context = {
        'article_list': article_list,
    }
    return render(request, 'index.html', context=context)


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

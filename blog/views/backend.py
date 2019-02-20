import os

from bs4 import BeautifulSoup

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect

from blog import models
from cnblog import settings


# 后台管理
@login_required
def cn_backend(request):
    article_list = models.Article.objects.filter(user=request.user)

    context = {
        'article_list': article_list
    }
    return render(request, 'backend/backend.html', context=context)


# 增加文章
@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        soup = BeautifulSoup(content, 'html.parser')
        # 过滤script,防止xss攻击
        for tag in soup.find_all():
            if tag.name == 'script':
                tag.decompose()

        # 获取文本进行截取，赋值给desc字段
        desc = soup.text[0:150] + '...'

        models.Article.objects.filter(user=request.user).create(
            title=title,
            user=request.user,
            desc=desc,
            content=str(soup)
        )

        return redirect(reverse('blog:backend'))

    return render(request, 'backend/add_article.html')


def upload(request):
    img = request.FILES.get('upload_img')
    path = os.path.join(settings.MEDIA_ROOT, 'add_article_img', img.name)
    with open(path, 'wb') as f:
        for line in img:
            f.write(line)

    response = {
        'error': 0,
        'url': f'/media/add_article_img/{img.name}'
    }

    return JsonResponse(response)

import os
import re

from bs4 import BeautifulSoup

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect

from blog import models
from blog.forms.articleForm import ArticleForm
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
    article_forms = ArticleForm()
    if request.method == 'POST':
        article_forms = ArticleForm(request.POST)
        if article_forms.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            category = request.POST.get('category')

            soup = BeautifulSoup(content, 'html.parser')

            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()
            desc = soup.text[0:150] + '...'

            models.Article.objects.filter(user=request.user).create(
                title=title,
                user=request.user,
                content=str(soup),
                desc=desc,
                category_id=category,

            )

            return redirect(reverse('blog:backend'))
        context = {
            'article_forms': article_forms,
        }
        return render(request, 'backend/add_article.html', context=context)
    context = {
        'article_forms': article_forms,
    }
    return render(request, 'backend/add_article.html', context=context)


# 编辑文章
@login_required
def edit_article(request, nid):
    article_obj = models.Article.objects.filter(nid=nid).first()
    article_forms = ArticleForm(instance=article_obj)

    if request.method == 'POST':
        article_forms = ArticleForm(request.POST, instance=article_obj)
        if article_forms.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            category = request.POST.get('category')

            soup = BeautifulSoup(content, 'html.parser')

            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()
            desc = soup.text[0:150] + '...'

            models.Article.objects.filter(user=request.user).update(
                title=title,
                user=request.user,
                content=str(soup),
                desc=desc,
                category_id=category,
            )
            return redirect(reverse('blog:backend'))

        context = {
            'article_forms': article_forms,
        }
        return render(request, 'backend/edit_article.html', context=context)

    context = {
        'article_forms': article_forms,
    }
    return render(request, 'backend/edit_article.html', context=context)


# 删除文章
@login_required
def delete_article(request, nid):
    response = {'status': False}
    nid = request.POST.get('nid')
    models.Article.objects.filter(nid=nid).delete()
    response['status'] = True
    return JsonResponse(response)


# 用户上传文件
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

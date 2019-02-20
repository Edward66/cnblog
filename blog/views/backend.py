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
    user = models.UserInfo.objects.filter(username=request.user.username).first()
    blog_obj = user.blog

    article_forms = ArticleForm()
    category_obj = models.Category.objects.filter(blog=blog_obj).all()
    if request.method == 'POST':
        article_forms = ArticleForm(request.POST)
        if article_forms.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            category_id = request.POST.get('category_id')
            tags = request.POST.get('tags')
            tags_list = re.split(',|，', tags)

            # 过滤script标签，防止xss攻击
            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()

            # 获取文本进行截取，赋值给desc字段
            article_forms.desc = soup.text[0:150] + '...'

            with transaction.atomic():
                # 增加文章
                article_obj = models.Article.objects.create(
                    title=title,
                    content=content,
                    category_id=category_id,
                    user=user
                )

                # 增加标签
                for tag in tags_list:
                    tag_obj = models.Tag.objects.create(
                        title=tag,
                        blog=blog_obj
                    )

                    # 增加文章标签关系表
                    models.Article2Tag.objects.create(
                        article=article_obj,
                        tag=tag_obj
                    )

            return redirect(reverse('blog:backend'))
        context = {
            'article_forms': article_forms,
            'category_obj': category_obj,
        }
        return render(request, 'backend/add_article.html', context=context)
    context = {
        'article_forms': article_forms,
        'category_obj': category_obj,
    }
    return render(request, 'backend/add_article.html', context=context)


# 编辑文章
@login_required
def edit_article(request, nid):
    user = models.UserInfo.objects.filter(username=request.user.username).first()
    blog_obj = user.blog
    edit_article_obj = models.Article.objects.filter(nid=nid).first()
    category_obj = models.Category.objects.filter(blog=blog_obj).all()

    # 返回到前端的已有信息
    title = edit_article_obj.title
    content = edit_article_obj.content

    data = {
        'title': title,
        'content': content,
    }

    article_forms = ArticleForm(data)

    if request.method == 'POST':
        article_forms = ArticleForm(request.POST, data)
        if article_forms.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            category_id = request.POST.get('category_id')

            # 过滤script标签，防止xss攻击
            soup = BeautifulSoup(content, 'html.parser')
            for tag in soup.find_all():
                if tag.name == 'script':
                    tag.decompose()

            # 获取文本进行截取，赋值给desc字段
            article_forms.desc = soup.text[0:150] + '...'

            models.Article.objects.filter(nid=nid).update(
                title=title,
                content=str(soup),
                category_id=category_id
            )

            return redirect(reverse('blog:backend'))

        context = {
            'article_forms': article_forms,
        }
        return render(request, 'backend/edit_article.html', context=context)

    context = {
        'edit_article_obj': edit_article_obj,
        'category_obj': category_obj,
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

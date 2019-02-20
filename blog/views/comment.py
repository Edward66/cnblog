import threading

from django.core.mail import send_mail
from django.db.models import F
from django.db import transaction
from django.http import JsonResponse

from blog import models
from cnblog import settings


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
        models.Comment.objects.filter(article_id=article_id).order_by('pk').values(
            'pk', 'content',
            'parent_comment_id',
            'user__username'
        ))

    # In order to allow non-dict objects to be serialized set the safe parameter to False.
    return JsonResponse(comment_obj, safe=False)

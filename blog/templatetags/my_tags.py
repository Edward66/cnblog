from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth

from blog import models

register = template.Library()


@register.inclusion_tag('classification.html')  # 先取数据，然后交给模板去渲染，最后返回模板
def get_classification_style(username):
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog

    category_list = models.Category.objects.filter(blog=blog).values('pk').annotate(
        count=Count('article__title')).values_list(
        'title', 'count')

    tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(count=Count('article')).values_list(
        'title', 'count'
    )

    date_list = models.Article.objects.filter(user=user).annotate(month=TruncMonth('created_time')).values_list(
        'month').annotate(
        count=Count('nid')).values_list(
        'month', 'count')

    context = {
        'username': username,
        'category_list': category_list,
        'tag_list': tag_list,
        'date_list': date_list
    }
    return context

from django.urls import path, re_path
from django.views.static import serve

from cnblog import settings
from blog.views import (
    backend, comment, functions, main
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

urlpatterns = [
    # 首页
    re_path(r'^$', main.index, name='index'),

    # 注册页面
    path('register/', functions.register, name='register'),

    # 文件上传
    path('upload/', backend.upload, name='upload'),

    # 登陆页面和滑动验证码
    path('login/', functions.login, name='login'),
    path('logout/', functions.logout, name='logout'),
    re_path(r'^pc-geetest/register', functions.slide_code_auth, name='pcgetcaptcha'),

    # 后台管理
    re_path('cn_backend/$', backend.cn_backend, name='backend'),
    re_path('cn_backend/add_article/$', backend.add_article, name='add_article'),

    # 点赞
    path('digg/', functions.digg),

    # 评论
    path('comment/', comment.comment),
    path('get_comment_tree/', comment.get_comment_tree),

    # media配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 主要以media开头，后面写什么都行

    # 文章详情页
    re_path(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)$', main.article_detail),

    # 个人站点的跳转
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$', main.home_site),

    # 个人站点
    re_path(r'^(?P<username>\w+)/$', main.home_site, name='home_site'),

]

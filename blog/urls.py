from django.urls import path, re_path
from django.views.static import serve

from blog import views
from blog.views import slide_code_auth
from cnblog import settings

SOCIAL_AUTH_URL_NAMESPACE = 'social'

urlpatterns = [
    # 首页
    re_path(r'^$', views.index, name='index'),

    # 注册页面
    path('register/', views.register, name='register'),

    # 文件上传
    path('upload/', views.upload, name='upload'),

    # 登陆页面和滑动验证码
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    re_path(r'^pc-geetest/register', slide_code_auth, name='pcgetcaptcha'),

    # 后台管理
    re_path('cn_backend/$', views.cn_backend, name='backend'),
    re_path('cn_backend/add_article/$', views.add_article, name='add_article'),

    # 点赞
    path('digg/', views.digg),

    # 评论
    path('comment/', views.comment),
    path('get_comment_tree/', views.get_comment_tree),

    # media配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 主要以media开头，后面写什么都行

    # 文章详情页
    re_path(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)$', views.article_detail),

    # 个人站点的跳转
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$', views.home_site),

    # 个人站点
    re_path(r'^(?P<username>\w+)/$', views.home_site, name='home_site'),

]

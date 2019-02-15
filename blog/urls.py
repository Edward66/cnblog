from django.urls import path, re_path
from django.views.static import serve

from blog import views
from blog.views import slide_code_auth
from cnblog import settings

SOCIAL_AUTH_URL_NAMESPACE = 'social'

urlpatterns = [
    # 首页
    re_path(r'index/', views.index, name='index'),

    # 登陆页面和滑动验证码
    path('login/', views.login, name='login'),
    re_path(r'^pc-geetest/register', slide_code_auth, name='pcgetcaptcha'),

    # 注册页面
    path('register/', views.register, name='register'),

    # media配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})  # 主要以media开头，后面写什么都行

]

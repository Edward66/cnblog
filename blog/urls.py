from django.urls import path, re_path

from blog import views
from blog.views import slide_code_auth

SOCIAL_AUTH_URL_NAMESPACE = 'social'

urlpatterns = [
    # 首页
    re_path('index/', views.index, name='index'),

    # 登陆页面和滑动验证码
    path('login/', views.login, name='login'),
    re_path(r'^pc-geetest/register', slide_code_auth, name='pcgetcaptcha'),

    # 注册页面
    path('register/', views.register, name='register')

]

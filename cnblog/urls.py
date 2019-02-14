from django.contrib import admin
from django.urls import path, re_path

from blog import views
from blog.views import slide_code_auth

SOCIAL_AUTH_URL_NAMESPACE = 'social'

urlpatterns = [
    path('admin/', admin.site.urls),

    # 首页
    re_path('index/', views.index, name='index'),

    # 滑动验证码
    path('login/', views.login),
    re_path(r'^pc-geetest/register', slide_code_auth, name='pcgetcaptcha'),

]

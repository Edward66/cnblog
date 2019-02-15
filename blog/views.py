from django.contrib import auth
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from blog.utils.slide_auth_code import pcgetcaptcha
from blog.forms.regForm import RegForm


# 登陆
def login(request):
    if request.method == "POST":
        response = {'user': None, 'msg': None}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')

        user = auth.authenticate(username=user, password=pwd)

        if user:
            auth.login(request, user)
            response['user'] = user.username
        else:
            response['msg'] = '用户名或密码错误'
        return JsonResponse(response)
    return render(request, 'login.html')


# 滑动验证码
def slide_code_auth(request):
    response_str = pcgetcaptcha(request)
    return HttpResponse(response_str)


# 首页
def index(request):
    return render(request, 'index.html')


# 注册页面
def register(request):
    form = RegForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context=context)

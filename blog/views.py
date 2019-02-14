import random

from django.contrib import auth
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from blog.utils.validCode import get_valid_code_img


def login(request):
    if request.method == 'POST':
        response = {'user': None, 'msg': None}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        valid_code = request.POST.get('valid_code')

        valid_code_str = request.session.get('valid_code_str')
        if valid_code.lower() == valid_code_str.lower():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)  # request.user == 当前登录对象
                response['user'] = user.username
            else:
                response['msg'] = '用户名或密码错误'
        else:
            response['msg'] = '验证码错误'
        return JsonResponse(response)
    return render(request, 'login.html')


def get_validCode_img(request):
    """
    基于PIL模块动态生成响应状态码图片
    :param request:
    :return:
    """
    data = get_valid_code_img(request)
    return HttpResponse(data)


def index(request):
    return render(request, 'index.html')

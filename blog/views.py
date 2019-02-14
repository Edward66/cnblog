import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from django.contrib import auth
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


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
                response['msg'] = 'usernmae or password wrongs'
        else:
            response['msg'] = 'valid code error!'
        return JsonResponse(response)
    return render(request, 'login.html')


def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_validCode_img(request):
    # 方式1：
    # with open('1.jpeg', 'rb') as f:
    #     data = f.read()
    # return HttpResponse(data)

    # 方式2（在硬盘上生成、读取图片）：
    # img = Image.new('RGB', (260, 34), color=get_random_color())
    #
    # with open('validCode.png', 'wb') as f:
    #     img.save(f, 'png')
    #
    # with open('validCode.png', 'rb') as f:
    #     data = f.read()
    #
    # return HttpResponse(data)

    # 方式3（在内存中生成、读取图片）：
    # img = Image.new('RGB', (260, 34), color=get_random_color())
    #
    # f = BytesIO()  # 用完之后，BytesIO会自动清掉
    # img.save(f, 'png')
    # data = f.getvalue()
    #
    # return HttpResponse(data)

    # 方式4（给image加文字）：
    img = Image.new('RGB', (260, 34), color=get_random_color())
    draw = ImageDraw.Draw(img)
    kumo_font = ImageFont.truetype('static/font/kumo.ttf', size=28)

    valid_code_str = ''
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_high_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_high_alpha])
        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=kumo_font)

        # 保存验证码字符串
        valid_code_str += random_char

    # 噪点噪线
    width = 260
    height = 34
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(5):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    # 保存验证码字符串到该用户的session
    request.session['valid_code_str'] = valid_code_str
    """
    1. asdasd12312asd 生成随机字符串
    2. COOKIE {"sessionid":asdasd12312asd}
    3. django-session
        session-key      session-data
        asdasd12312asd       {"valid_code_str:'12345"}
    """

    f = BytesIO()  # 用完之后，BytesIO会自动清掉
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)


def index(request):
    return render(request, 'index.html')

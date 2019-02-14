import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from django.shortcuts import render, HttpResponse


def login(request):
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

    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_high_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_high_alpha])
        draw.text((i * 50 + 20, 5), random_char, get_random_color(), font=kumo_font)

        # draw.line()  # 画线
        # draw.point()  # 画点

    # 噪点噪线
    width = 260
    height = 34
    for i in range(10):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(10):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    f = BytesIO()  # 用完之后，BytesIO会自动清掉
    img.save(f, 'png')
    data = f.getvalue()

    return HttpResponse(data)

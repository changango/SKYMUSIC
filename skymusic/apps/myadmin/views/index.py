from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from myadmin.models import users


# 后台管理首页
def index(requset):

    return render(requset,'myadmin/index/index.html')


# 后台登录首页
def login(requset):
    return render(requset, 'myadmin/index/login.html')


# 执行登录首页
def dologin(requset):
    try:
        # 执行验证码的验证
        if requset.POST['code'] != requset.session['verificationcode']:
            context = {'info': "验证码错误！"}
            return render(requset, 'myadmin/index/login.html', context)
        user = users.objects.get(username=requset.POST['username'])
        if user.status == 0:
            import hashlib
            md5 = hashlib.md5()
            s = requset.POST['password'] + user.password_salt
            md5.update(s.encode('utf-8')) # 将产生的MD5的字串放进去
            if user.password_hash == md5.hexdigest():
                requset.session['adminuser'] = user.toDict()
                return redirect(reverse("myadmin_index"))
            else:
                context = {"info": "账号或密码错误！"}
        else:
            context = {'info': "账号或密码错误！"}
    except Exception as error:
        print(error)
        context = {'info':"账号或密码错误！"}
    return render(requset,'myadmin/index/login.html',context)

# 后台管理首页
def logout(requset):
    del requset.session['adminuser']
    return redirect(reverse("myadmin_login"))

# 输出验证码
def verificationcode(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100),100)
    width = 100
    height = 35
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    font = ImageFont.truetype('static/fonts/Inkfree.ttf', 21)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    draw.text((5, 5), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 5), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 5), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 5), rand_str[3], font=font, fill=fontcolor)
    del draw
    request.session['verificationcode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')
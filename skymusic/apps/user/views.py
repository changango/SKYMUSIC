import os
from datetime import datetime
from django import forms
from django.contrib import auth
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from index.models import users, comment, cltsinger, singersort, songs, songsort, dynamic, friends
from index.models import cltmusic, singers
from .forms import EnrollForm
import filetype
# Create your views here.

from skymusic.settings import BASE_DIR


# 音乐文件上传函数
def upload_song(request, file):
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    filepath = '/static/songs/' + obj.name
    s = os.path.join(BASE_DIR, 'static', 'songs', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    songtype = filetype.guess(s)
    context = {'filename': obj.name, 'songpath': filepath, 'songtype': songtype.extension}
    return context


# 歌词文件上传函数
def upload_lyrics(request, file):
    print(1)
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    s = os.path.join(BASE_DIR, 'static', 'songs-lyrics', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    context = {'filename': obj.name}
    return context


# 图片上传函数
def upload_singer_img(request, file):
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    filepath = '/static/singers-images/' + obj.name
    s = os.path.join(BASE_DIR, 'static', 'singers-images', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    imgtype = filetype.guess(s)
    context = {'imgpath': filepath, 'imgtype': imgtype.extension}
    return context


# 音乐人主页信息展示
def musicsingerindex(request, uid):
    user = request.session.get('musicuser', [])
    musicsingeruser = singers.objects.get(singers_id=user['musicsinger'])
    mymusic = songs.objects.filter(singerinfo_id=musicsingeruser.singers_id)
    number = mymusic.count()
    return render(request, 'index/user/musicsinger/musicsingerindex.html', locals())


# 成为音乐人
def musicsinger(request, uid):
    singersortlist = singersort.objects.all().order_by('singersort_id')
    if request.method == 'POST':
        try:
            ob = singers()
            ob.singername = request.POST['singername']
            ob.sex = request.POST['sex']

            # 歌手图片文件信息导入mysql
            pic = upload_singer_img(request, 'singerpicture')
            ob.singerpicture = pic['imgpath']

            sort = request.POST['singersortname']
            ss = singersort.objects.get(singersortname=sort)
            ob.singertype = ss
            ob.englishname = request.POST['englishname']
            ob.nationality = request.POST['nationality']
            ob.birthplace = request.POST['birthplace']
            ob.birthdate = request.POST['birthdate']
            ob.personalintroduction = request.POST['personalintroduction']
            ob.save()
            usermin = users.objects.get(users_id=uid)
            usermin.musicsinger = ob
            usermin.save()
            request.session['musicuser'] = usermin.toDict()
            info = "音乐人注册成功！"
        except Exception as error:
            print(error)
            info = "音乐人注册失败！"
    return render(request, 'index/user/musicsinger/musicsinger.html', locals())


# 上传音乐人音乐
def music_upload(request, uid):
    songsortlist = songsort.objects.all()
    user = request.session.get('musicuser', [])
    musicsingeruser = singers.objects.get(singers_id=user['musicsinger'])
    singer = singers.objects.get(singers_id=musicsingeruser.singers_id)
    if request.method == 'POST':
        try:
            ob = songs()
            ob.songname = request.POST['songname']

            # 在Dynamic表中同步歌曲信息
            ob.singername = request.POST['singername']
            ob.songlanguages = request.POST['songlanguages']
            ob.songsource = request.POST['songsource']
            sort = request.POST['songsortname']

            ss = songsort.objects.get(songsortname=sort)
            ob.songtype = ss

            # 图片文件信息导入mysql
            pic = upload_img(request, 'songpicture')
            ob.songpicture = pic['imgpath']
            ob.songimgtype = pic['imgtype']

            # 歌曲文件信息导入mysql
            song = upload_song(request, 'songfile')
            ob.filename = song['filename']
            ob.songfile = song['songpath']
            ob.songfiletype = song['songtype']

            # 歌词文件信息导入mysql upload_lyrics
            lyrics = upload_lyrics(request, 'songlyrics')
            ob.songlyrics = lyrics['filename']

            ob.releasetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.updatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ob.singerinfo = singer

            ob.save()
            Dynamic = dynamic()
            Dynamic.song = ob
            Dynamic.songname = ob.songname
            Dynamic.plays = 0
            Dynamic.search = 0
            Dynamic.down = 0
            Dynamic.save()
            info = '添加成功！'
        except Exception as error:
            print(error)
            info = "添加失败！"
    return render(request, 'index/user/musicsinger/musicsingersong.html', locals())


# 修改音乐人信息
def musicsingerinfo(request, uid):
    user = request.session.get('musicuser', [])
    if request.method == 'POST':
        try:
            ob = singers.objects.get(singers_id=user['musicsinger'])
            ob.singername = request.POST['singername']
            ob.sex = request.POST['sex']

            sort = request.POST['singersortname']
            ss = singersort.objects.get(singersortname=sort)
            ob.singertype = ss

            # 歌手图片信息修改
            pic = upload_img(request, 'singerpicture')
            if pic:
                ob.singerpicture = pic['imgpath']

            ob.englishname = request.POST['englishname']
            ob.nationality = request.POST['nationality']
            ob.birthplace = request.POST['birthplace']
            ob.birthdate = request.POST['birthdate']
            ob.personalintroduction = request.POST['personalintroduction']

            ob.save()
            info = '修改成功！'
        except Exception as error:
            print(error)
            info = '修改失败！'
    singer = singers.objects.get(singers_id=user['musicsinger'])
    singersortlist = singersort.objects.all()
    ss = singersort.objects.get(singersort_id=singer.singertype_id)
    ssn = ss.singersortname
    return render(request, 'index/user/musicsinger/musicsingerinfo.html', locals())


def upload_img(request, file):
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    filepath = '/static/users-images/' + obj.name
    s = os.path.join(BASE_DIR, 'static', 'users-images', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    imgtype = filetype.guess(s)
    context = {'imgpath': filepath, 'imgtype': imgtype.extension}
    return context


# 登录
def login(request):
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return render(request, 'index/user/login.html')


# 执行登录
def dologin(requset):
    try:
        # 执行验证码的验证
        if requset.POST['code'] != requset.session['verifcode']:
            context = {'info': "验证码错误！"}
            return render(requset, 'index/user/login.html', context)
        user = users.objects.get(username=requset.POST['username'])

        if user.status == 1:
            import hashlib
            md5 = hashlib.md5()
            s = requset.POST['password'] + user.password_salt
            md5.update(s.encode('utf-8'))  # 将产生的MD5的字串放进去
            if user.password_hash == md5.hexdigest():
                requset.session['musicuser'] = user.toDict()
                return HttpResponseRedirect(requset.session['login_from'])
            else:
                context = {"info": "账号或密码错误！"}
        else:
            context = {'info': "账号或密码错误！"}
    except Exception as error:
        print(error)
        context = {'info': "账号或密码错误！"}
    return render(requset, 'index/user/login.html', context)


# 修改个人信息
def useredit(request, uid):
    try:
        ob = users.objects.get(users_id=uid)
        return render(request, 'index/user/userinfoedit.html', locals())
    except Exception as error:
        info = '没有找到要修改的用户信息！'
        return render(request, 'index/user/userinfoedit.html', locals())


def douseredit(request, uid):
    if request.method == 'POST':
        try:
            ob = users.objects.get(users_id=uid)
            ob.username = request.POST['username']
            ob.nickname = request.POST['nickname']
            ob.sex = request.POST['sex']

            # 修改头像
            pic = upload_img(request, 'headprotrait')
            if pic:
                ob.headprotrait = pic['imgpath']

            s = request.POST['password']
            if s:
                import hashlib, random
                md5 = hashlib.md5()
                n = random.randint(100000, 999999)
                x = s + str(n)
                md5.update(x.encode('utf-8'))
                ob.password_hash = md5.hexdigest()
                ob.password_salt = n
            ob.save()
            info = '修改成功！'
        except Exception as error:
            info = '修改失败！'
    return render(request, 'index/user/userinfoedit.html', locals())


# 退出登录
def logout(request):
    del request.session['musicuser']
    try:
        del request.session['login_from']
    except Exception as error:
        pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


# 注册
def enroll(request):
    enroll_form = EnrollForm()
    return render(request, 'index/user/enroll.html', locals())


def doenroll(request):
    enroll_form = EnrollForm(request.POST)
    if enroll_form.is_valid():
        ob = users()
        ob.username = enroll_form.cleaned_data['username']
        ob.nickname = enroll_form.cleaned_data['nickname']
        ob.is_status = 'offline'
        import hashlib, random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        x = enroll_form.cleaned_data['password1'] + str(n)
        print(enroll_form.cleaned_data['password1'])
        md5.update(x.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.status = int(1)
        ob.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': '注册成功'}
        return render(request, 'index/user/login.html', context)
    else:
        info = enroll_form.errors['__all__'][0]
        enroll_form = EnrollForm()
        return render(request, 'index/user/enroll.html', locals())


def myuser(request):
    user = request.session.get('musicuser', [])
    if user:
        lovesong_list = cltmusic.objects.filter(cltmusic_user_id=user['users_id']).all()
        return render(request, 'index/user/myuser.html', locals())
    else:
        return render(request, 'index/user/havuser.html', locals())


def parcomment(request):
    user = request.session.get('musicuser', [])
    commentsong_list = comment.objects.filter(commentuser_id=user['users_id']).all()
    return render(request, 'index/user/parcomment.html', locals())


def parsinger(request):
    user = request.session.get('musicuser', [])
    parsinger_list = cltsinger.objects.filter(cltsinger_user_id=user['users_id']).all()
    return render(request, 'index/user/parsinger.html', locals())


# 验证码
def verifcode(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 100)
    width = 100
    height = 35
    im = Image.new('RGB', (width, height), bgcolor)
    draw = ImageDraw.Draw(im)
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
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
    request.session['verifcode'] = rand_str
    import io
    buf = io.BytesIO()
    im.save(buf, 'png')
    return HttpResponse(buf.getvalue(), 'image/png')


# 好友
def friend(request, uid):
    friend_list = friends.objects.filter(
        Q(Q(friend_user1_status=1) & Q(friend_user2_status=1) & (Q(friend_user1_id=uid) | Q(friend_user2_id=uid))))
    return render(request, 'chat/friend.html', locals())


# 关注
def attention(request, uid):
    friend_list = friends.objects.filter(
        Q(Q(friend_user1_id=uid) & Q(friend_user1_status=1)) & Q(friend_user2_status=0) |
        Q(Q(friend_user2_id=uid) & Q(friend_user2_status=1)) & Q(friend_user1_status=0))
    return render(request, 'chat/attention.html', locals())


# 粉丝
def fans(request, uid):
    friend_list = friends.objects.filter(Q(Q(friend_user1_id=uid) & Q(friend_user1_status=0)) |
                                         Q(Q(friend_user2_id=uid) & Q(friend_user2_status=0)))
    return render(request, 'chat/fans.html', locals())


# 删除好友
def del_friend(request, uid):
    mymusic_id = request.session.get('musicuser', [])
    target_user_id = mymusic_id['users_id']
    user1 = users.objects.get(users_id=target_user_id)
    friend_user = friends.objects.get(Q(Q(friend_user1_id=uid) & Q(friend_user2_id=target_user_id)) |
                                      Q(Q(friend_user2_id=uid) & Q(friend_user1_id=target_user_id)))
    if friend_user.friend_user1 == user1:
        friend_user.friend_user1_status = 0
    elif friend_user.friend_user2 == user1:
        friend_user.friend_user2_status = 0
    friend_user.save()
    friend_list = friends.objects.filter(
        Q(Q(friend_user1_status=1) & Q(friend_user2_status=1) & (
                    Q(friend_user1_id=target_user_id) | Q(friend_user2_id=target_user_id))))
    return render(request, 'chat/friend.html', locals())


# 取消关注
def del_attention(request, uid):
    mymusic_id = request.session.get('musicuser', [])
    target_user_id = mymusic_id['users_id']
    friend_user = friends.objects.get(Q(Q(friend_user1_id=target_user_id)&Q(friend_user1_status=1)&Q(friend_user2_id=uid)&Q(friend_user2_status=0))|
                                      Q(Q(friend_user2_id=target_user_id)&Q(friend_user2_status=1)&Q(friend_user1_id=uid)&Q(friend_user1_status=0))).delete()
    friend_list = friends.objects.filter(
        Q(Q(friend_user1_id=target_user_id) & Q(friend_user1_status=1)) & Q(friend_user2_status=0) |
        Q(Q(friend_user2_id=target_user_id) & Q(friend_user2_status=1)) & Q(friend_user1_status=0))
    return render(request, 'chat/attention.html', locals())


# 添加好友
def add_friend(request, uid):
    mymusic_id = request.session.get('musicuser', [])
    target_user_id = mymusic_id['users_id']
    friend_user = friends.objects.get(Q(Q(friend_user1_id=target_user_id)&Q(friend_user1_status=0)&Q(friend_user2_id=uid)&Q(friend_user2_status=1))|
                                      Q(Q(friend_user1_id=uid)&Q(friend_user1_status=1)&Q(friend_user2_id=target_user_id)&Q(friend_user2_status=0)))
    if friend_user.friend_user1_status == 0:
        friend_user.friend_user1_status = 1
    elif friend_user.friend_user2_status == 0:
        friend_user.friend_user2_status = 1
    friend_user.save()
    friend_list = friends.objects.filter(Q(Q(friend_user1_id=target_user_id) & Q(friend_user1_status=0)) |
                                         Q(Q(friend_user2_id=target_user_id) & Q(friend_user2_status=0)))
    return render(request, 'chat/fans.html', locals())
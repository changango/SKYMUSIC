from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from myadmin.models import songs, singers
from myadmin.models import dynamic
from myadmin.models import songsort

import os
import filetype



from skymusic.settings import BASE_DIR

# 图片文件上传函数
def upload_img(request, file):
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    filepath = '/static/songs-images/' + obj.name
    s = os.path.join(BASE_DIR, 'static', 'songs-images', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    imgtype = filetype.guess(s)
    context = {'imgpath': filepath, 'imgtype': imgtype.extension}
    return context


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
    context = {'filename':obj.name, 'songpath': filepath, 'songtype': songtype.extension}
    return context

# 歌词文件上传函数
def upload_lyrics(request, file):
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    s = os.path.join(BASE_DIR, 'static', 'songs-lyrics', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    context = {'filename':obj.name}
    return context

# 歌曲管理
def index(request, pindex=1):
    umod = songs.objects.all().order_by('songs_id')
    slist = umod.all()

    # 关键字搜索
    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        slist = slist.filter(Q(songname__contains=kw) | Q(songsinger__contains=kw))
        mywhere.append('key=' + kw)

    # 分页处理
    pindex = int(pindex)
    page = Paginator(slist, 5)
    maxpages = page.num_pages

    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    list1 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'songlist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/song/index.html', context)


def add(request,sid):
    songsortlist = songsort.objects.all()
    singer = singers.objects.get(singers_id=sid)
    return render(request, 'myadmin/song/add.html', locals())

def insert(request,sid):
    try:
        ob = songs()

        ob.songname = request.POST['songname']

        # 在Dynamic表中同步歌曲信息
        ob.singername = request.POST['singername']
        ob.songlanguages = request.POST['songlanguages']
        ob.songsource = request.POST['songsource']
        sort = request.POST['songsortname']

        ss = songsort.objects.get(songsortname=sort)
        print(ss.songsortname)
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
        s = singers.objects.get(singers_id=sid)
        ob.singerinfo = s
        ob.save()
        Dynamic = dynamic()
        Dynamic.song = ob
        Dynamic.songname = ob.songname
        Dynamic.plays = 0
        Dynamic.search = 0
        Dynamic.down = 0
        Dynamic.save()
        context = {'info': "添加成功！"}
    except Exception as error:
        print(error)
        context = {'info': "添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    try:
        ob = songs.objects.filter(songs_id=uid).delete()
        context = {'info': "删除成功！"}
    except Exception as error:
        print(error)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    try:
        ob = songs.objects.get(songs_id=uid)
        songsortlist = songsort.objects.all().order_by('songsort_id')
        ss = songsort.objects.get(songsort_id=ob.songtype_id)
        ssn = ss.songsortname
        context = {'song': ob, 'songsortlist': songsortlist, 'ssn': ssn}
        return render(request, 'myadmin/song/edit.html', context)
    except Exception as error:
        print(error)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', context)


def update(request, uid=0):
    try:
        ob = songs.objects.get(songs_id=uid)
        ob.songname = request.POST['songname']
        ob.singername = request.POST['singername']
        ob.songsource = request.POST['songsource']

        sort = request.POST['songsortname']
        ss = songsort.objects.get(songsortname=sort)
        ob.songtype = ss

        # 图片信息修改
        pic = upload_img(request, 'songpicture')
        if pic:
            ob.songpicture = pic['imgpath']
            ob.songimgtype = pic['imgtype']

        # 歌曲信息修改
        song = upload_song(request, 'songfile')
        if song:
            ob.filename = song['filename']
            ob.songfile = song['songpath']
            ob.songfiletype = song['songtype']

        # 歌词文件修改
        lyrics = upload_lyrics(request, 'songlyrics')
        if lyrics:
            ob.songlyrics = lyrics['filename']

        ob.updatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()
        context = {'info': '修改成功！'}
    except Exception as error:
        print(error)
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)

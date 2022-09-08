from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
import datetime

from myadmin.models import singers, songs
from myadmin.models import singersort

import os

from skymusic.settings import BASE_DIR


def upload_img(request, file):
    if request.method == 'POST':
        obj = request.FILES.get(file)
    if not obj:
        return 0
    filepath = '/static/singers-images/' + obj.name
    s = os.path.join(BASE_DIR, 'static', 'singers-images', obj.name)
    f = open(s, 'wb')
    for chunk in obj.chunks():  # 分片写入
        f.write(chunk)
    context = {'imgpath': filepath}
    return context


def index(request, pindex=1):
    simod = singers.objects.all().order_by('singers_id')
    silist = simod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        silist = silist.filter(Q(singername__contains=kw) | Q(englishname__contains=kw))
        mywhere.append('key=' + kw)

    pindex = int(pindex)
    page = Paginator(silist, 4)
    maxpages = page.num_pages
    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list1 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'singerlist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/singer/index.html', context)


def add(request):
    singersortlist = singersort.objects.all().order_by('singersort_id')
    context = {'singersortlist': singersortlist}
    return render(request, 'myadmin/singer/add.html', context)


def insert(request):
    try:
        ob = singers()
        ob.singername = request.POST['singername']
        ob.sex = request.POST['sex']

        # 歌手图片文件信息导入mysql
        pic = upload_img(request, 'singerpicture')
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
        context = {'info': "添加成功！"}
    except Exception as error:
        print(error)
        context = {'info': "添加失败！"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    try:
        id = request
        ob = singers.objects.filter(singers_id=uid).delete()
        context = {'info': "删除成功！"}
    except Exception as error:
        print(error)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    try:
        ob = singers.objects.get(singers_id=uid)
        singersortlist = singersort.objects.all().order_by('singersort_id')
        ss = singersort.objects.get(singersort_id=ob.singertype_id)
        ssn = ss.singersortname
        context = {'singer': ob, 'singersortlist': singersortlist, 'ssn': ssn}
        return render(request, 'myadmin/singer/edit.html', context)
    except Exception as error:
        print(error)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', context)


def update(request, uid=0):
    try:
        ob = singers.objects.get(singers_id=uid)
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
        context = {'info': '修改成功！'}
    except Exception as error:
        print(error)
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)


def singerinfo(request, sid):
    singer = singers.objects.get(singers_id=sid)
    song = songs.objects.filter(singername=singer.singername).all()
    number = song.count()
    return render(request, 'myadmin/singer/singerinfo.html', locals())

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from myadmin.models import songs
from myadmin.models import dynamic
from myadmin.models import songsort
from myadmin.models import singersort


def index(request, pindex=1):
    umod = songsort.objects.all().order_by('songsort_id')
    sslist = umod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        sslist = sslist.filter(Q(songsortname__contains=kw))
        mywhere.append('key=' + kw)

    # 分页处理
    pindex = int(pindex)
    page = Paginator(sslist, 5)
    maxpages = page.num_pages

    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    list1 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'songsortlist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/songtype/songsort.html', context)

def add(request):
    return render(request, 'myadmin/songtype/add.html')

def insert(requset):
    try:
        ob = songsort()
        ob.songsortname = requset.POST['songsortname']
        ob.save()
        context = {'info': "添加成功！"}
    except Exception as error:
        print(error)
        context = {'info': "添加失败！"}
    return render(requset, "myadmin/info.html", context)

def delete(request, uid=0):
    try:
        ob = songsort.objects.filter(songsort_id=uid).delete()
        context = {'info': "删除成功！"}
    except Exception as error:
        print(error)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    try:
        ob = songsort.objects.get(songsort_id=uid)
        context = {'songsortlist':ob}
        return render(request, 'myadmin/songtype/edit.html',context)
    except Exception as error:
        print(error)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', context)


def update(request, uid=0):
    try:
        ob = songsort.objects.get(songsort_id=uid)
        ob.songsortname = request.POST['songsortname']
        ob.save()
        context = {'info': '修改成功！'}
    except Exception as error:
        print(error)
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)

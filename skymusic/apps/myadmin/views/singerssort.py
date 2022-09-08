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
    umod = singersort.objects.all().order_by('singersort_id')
    sslist = umod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        sslist = sslist.filter(Q(singersortname__contains=kw))
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
    context = {'singersortlist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/singertype/singersort.html', context)

def add(request):
    return render(request, 'myadmin/singertype/add.html')

def insert(requset):
    try:
        ob = singersort()
        ob.singersortname = requset.POST['singersortname']
        ob.save()
        context = {'info': "添加成功！"}
    except Exception as error:
        print(error)
        context = {'info': "添加失败！"}
    return render(requset, "myadmin/info.html", context)

def delete(request, uid=0):
    try:
        ob = singersort.objects.filter(singersort_id=uid).delete()
        context = {'info': "删除成功！"}
    except Exception as error:
        print(error)
        context = {'info': "删除失败！"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    try:
        ob = singersort.objects.get(singersort_id=uid)
        context = {'singersortlist':ob}
        return render(request, 'myadmin/singertype/edit.html',context)
    except Exception as error:
        print(error)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', context)


def update(request, uid=0):
    try:
        ob = singersort.objects.get(singersort_id=uid)
        ob.singersortname = request.POST['singersortname']
        ob.save()
        context = {'info': '修改成功！'}
    except Exception as error:
        print(error)
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)


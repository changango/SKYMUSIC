from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
import datetime

from myadmin.models import dynamic


# 排行榜所有歌曲信息 按照id排序
def index(request, pindex=1):
    dymod = dynamic.objects.order_by('dynamic_id').all()
    dylist = dymod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        dylist = dylist.filter(Q(songname__contains=kw))
        mywhere.append('key=' + kw)

    pindex = int(pindex)
    page = Paginator(dylist, 5)
    maxpages = page.num_pages
    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list1 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'dynamiclist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/dynamic/index.html', context)


# 按照播放次数plays rank 显示歌曲信息
def playsrank(request, pindex=1):
    prmod = dynamic.objects.order_by('-plays').all()
    prlist = prmod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        prlist = prlist.filter(Q(songname__contains=kw))
        mywhere.append('key=' + kw)

    pindex = int(pindex)
    page = Paginator(prlist, 5)
    maxpages = page.num_pages
    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list1 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'playsranklist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/dynamic/plays-rank.html', context)


# 按照搜索次数search rank 显示歌曲信息
def searchrank(request, pindex=1):
    srmod = dynamic.objects.order_by('-search').all()
    srlist = srmod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        srlist = srlist.filter(Q(songname__contains=kw))
        mywhere.append('key=' + kw)

    pindex = int(pindex)
    page = Paginator(srlist, 5)
    maxpages = page.num_pages
    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list1 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'searchranklist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/dynamic/search-rank.html', context)

# 按照下载次数down rank 显示歌曲信息
def downrank(request,pindex=1):
    drmod = dynamic.objects.order_by('-down').all()
    drlist = drmod.all()

    mywhere = []
    kw = request.GET.get("key", None)
    if kw:
        drlist = drlist.filter(Q(songname__contains=kw))
        mywhere.append('key=' + kw)

    pindex = int(pindex)
    page = Paginator(drlist, 5)
    maxpages = page.num_pages
    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list1 = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'downranklist': list1, 'plist': plist, 'pindex': pindex, 'maxpages': maxpages, 'mywhere': mywhere}
    return render(request, 'myadmin/dynamic/down-rank.html', context)

# 修改排行榜中的信息
def editrank(request,uid=0):
    try:
        ob = dynamic.objects.get(dynamic_id=uid)
        context = {'dynamic': ob}
        return render(request, 'myadmin/dynamic/edit-rank.html', context)
    except Exception as error:
        print(error)
        context = {'info': "没有找到要修改的信息！"}
        return render(request, 'myadmin/info.html', context)

# 更新排行榜中的信息
def updaterank(request, uid=0):
    try:
        ob = dynamic.objects.get(dynamic_id=uid)
        ob.plays = request.POST['plays']
        ob.search = request.POST['search']
        ob.down = request.POST['down']
        ob.save()
        context = {'info': '修改成功！'}
    except Exception as error:
        print(error)
        context = {'info': '修改失败！'}
    return render(request, 'myadmin/info.html', context)
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from index.models import songs
from index.models import dynamic
from index.models import singers


def index(request, pindex=1):
    # 新歌首发-最新
    song = songs.objects.order_by('-releasetime').all().values()
    for i in song:
        id = singers.objects.get(singername=i['singername']).singers_id
        i['singers_id'] = id

    pindex = int(pindex)
    page = Paginator(song, 4)
    maxpages = page.num_pages

    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    songlist = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    context = {'song': songlist, 'plist': plist, 'pindex': pindex, 'pp': "url 'index' pindex|add:-1",
               'np': "url 'index' pindex|add:1"}
    return render(request, 'index/index.html', context)


def nevindex(request):
    return index(request, 1)


# 最新歌曲
def new(request, pindex=1):
    song = songs.objects.order_by('-releasetime').all().values()
    for i in song:
        id = singers.objects.get(singername=i['singername']).singers_id
        i['singers_id'] = id

    pindex = int(pindex)
    page = Paginator(song, 4)
    maxpages = page.num_pages

    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    songlist = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'song': songlist, 'plist': plist, 'pindex': pindex}

    return render(request, 'index/newnav/new.html', context)


# 最新内地排行
def inland(request, pindex=1):
    song = songs.objects.all().filter(songsource='内地').order_by('releasetime').values()
    for i in song:
        id = singers.objects.get(singername=i['singername']).singers_id
        i['singers_id'] = id

    pindex = int(pindex)
    page = Paginator(song, 4)
    maxpages = page.num_pages

    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    songlist = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'song': songlist, 'plist': plist, 'pindex': pindex}
    return render(request, 'index/newnav/inland.html', context)
    # return render(request, 'index/index.html')


# 最新港台
def rthk(request, pindex=1):
    song = songs.objects.all().filter(songsource='港台').order_by('releasetime').values()
    for i in song:
        id = singers.objects.get(singername=i['singername']).singers_id
        i['singers_id'] = id

    pindex = int(pindex)
    page = Paginator(song, 4)
    maxpages = page.num_pages

    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    songlist = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'song': songlist, 'plist': plist, 'pindex': pindex}
    return render(request, 'index/newnav/rthk.html', context)


# 最新欧美
def europe(request, pindex=1):
    song = songs.objects.all().filter(songsource='欧美').order_by('releasetime').values()
    for i in song:
        id = singers.objects.get(singername=i['singername']).singers_id
        i['singers_id'] = id

    pindex = int(pindex)
    page = Paginator(song, 4)
    maxpages = page.num_pages

    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    songlist = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'song': songlist, 'plist': plist, 'pindex': pindex}
    return render(request, 'index/newnav/europe.html', context)


# 最新韩国
def korea(request, pindex=1):
    song = songs.objects.all().filter(songsource='韩国').order_by('releasetime').values()
    for i in song:
        id = singers.objects.get(singername=i['singername']).singers_id
        i['singers_id'] = id

    pindex = int(pindex)
    page = Paginator(song, 4)
    maxpages = page.num_pages

    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    songlist = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'song': songlist, 'plist': plist, 'pindex': pindex}
    return render(request, 'index/newnav/korea.html', context)


# 最新日本
def japanese(request, pindex=1):
    song = songs.objects.all().filter(songsource='日本').order_by('releasetime').values()
    for i in song:
        id = singers.objects.get(singername=i['singername']).singers_id
        i['singers_id'] = id

    pindex = int(pindex)
    page = Paginator(song, 4)
    maxpages = page.num_pages

    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1

    songlist = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息
    context = {'song': songlist, 'plist': plist, 'pindex': pindex}
    return render(request, 'index/newnav/japanese.html', context)

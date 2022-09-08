from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

from index.models import singers
from index.models import songsort
from index.models import songs


def song(request, pindex=1):
    ssort = songsort.objects.all()
    songtype = request.GET.get('type', '')
    if songtype:
        song_info = songs.objects.select_related('songtype').filter(songtype__songsortname=songtype).all()
    else:
        song_info = songs.objects.all()

    number = song_info.count()
    # 分页处理
    pindex = int(pindex)
    page = Paginator(song_info, 7)
    maxpages = page.num_pages
    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    song = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    return render(request, 'index/song/song.html', locals())

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

from index.models import songs, singers
from index.models import dynamic


def rank(requset):
    # 排行榜-新歌榜
    new_songs = songs.objects.order_by('-releasetime').all()[:5]
    # 排行榜-热歌榜
    plays_songs = dynamic.objects.select_related('song').all().order_by('-plays')[:5]
    # 排行榜-搜索榜
    search_songs = dynamic.objects.select_related('song').all().order_by('-search')[:5]
    # 排行榜-下载榜
    down_songs = dynamic.objects.select_related('song').all().order_by('-down')[:5]

    return render(requset, 'index/rank/rank.html', locals())


def rankinfo(requset,pindex=1):
    type = [{'type':'new','typename':'新歌榜'},{'type':'play','typename':'热歌榜'},{'type':'search','typename':'搜索榜'},{'type':'down','typename':'下载榜'}]
    songtype = requset.GET.get('type', '')
    if songtype == 'play':
        song_info = dynamic.objects.select_related('song').all().order_by('-plays').values()
        for i in song_info:
            # print(i['song_id']['singername'])
            sname = songs.objects.get(songs_id=i['song_id']).singername
            s= singers.objects.get(singername=sname)
            i['singers_id'] = s.singers_id
            i['singername'] = s.singername
    elif songtype == 'search':
        song_info = dynamic.objects.select_related('song').all().order_by('-search').values()
        for i in song_info:
            # print(i['song_id']['singername'])
            sname = songs.objects.get(songs_id=i['song_id']).singername
            s = singers.objects.get(singername=sname)
            i['singers_id'] = s.singers_id
            i['singername'] = s.singername
    elif songtype == 'down':
        song_info = dynamic.objects.select_related('song').all().order_by('-down').values()
        for i in song_info:
            # print(i['song_id']['singername'])
            sname = songs.objects.get(songs_id=i['song_id']).singername
            s = singers.objects.get(singername=sname)
            i['singers_id'] = s.singers_id
            i['singername'] = s.singername
    elif songtype == 'new':
        song_info = songs.objects.order_by('-releasetime').all().values()
        for i in song_info:
            id = singers.objects.get(singername=i['singername']).singers_id
            i['singers_id'] = id
            i['song_id'] = i['songs_id']
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

    return render(requset, 'index/rank/rankinfo.html', locals())


from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

from index.models import singers, cltsinger, users
from index.models import singersort
from index.models import songs


def singer(request, pindex=1):
    ssort = singersort.objects.all()
    singertype = request.GET.get('type', '')
    if singertype:
        singer_info = singers.objects.select_related('singertype').filter(singertype__singersortname=singertype).all()
    else:
        singer_info = singers.objects.all()

    # 分页处理
    pindex = int(pindex)
    page = Paginator(singer_info, 4)
    maxpages = page.num_pages
    # 判断当前页面是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    singer = page.page(pindex)  # 获取当前页数据
    plist = page.page_range  # 获取页码列表信息

    return render(request, 'index/singer/singer.html', locals())


def singerinfo(request, sid):
    singer = singers.objects.get(singers_id=sid)
    song = songs.objects.filter(singername=singer.singername).all()
    number = song.count()

    # 关注
    user = request.session.get('musicuser', [])

    if user:
        try:
            cltmusic_list = cltsinger.objects.get(cltsinger_user_id=user['users_id'], cltsinger_singer_id=sid)
            request.session['cltsinger_id'] = 1
        except Exception as error:
            print(error)
            request.session['cltsinger_id'] = 0

    return render(request, 'index/singer/singerinfo.html', locals())


def cltsingers(request, sid):
    cltsinger_id = request.session.get('cltsinger_id', [])
    if cltsinger_id == 0:
        ob = cltsinger()
        user = request.session.get('musicuser', [])
        u = users.objects.get(users_id=user['users_id'])
        ob.cltsinger_user = u
        s = singers.objects.get(singers_id=sid)
        ob.cltsinger_singer = s
        ob.save()
        request.session['cltsinger_id'] = 1
    elif cltsinger_id == 1:
        user = request.session.get('musicuser', [])
        ob = cltsinger.objects.get(cltsinger_user_id=user['users_id'], cltsinger_singer_id=sid).delete()
        request.session['cltsinger_id'] = 0
    return singerinfo(request, sid)

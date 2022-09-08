from django.http import StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt

from index.models import songs
from index.models import dynamic
from index.models import comment
from index.models import users
from index.models import cltmusic


@csrf_exempt
def musicplayer(request, sid):
    song = songs.objects.get(songs_id=sid)

    playlist = request.session.get('playlist', [])
    song_exist = False
    if playlist:
        for i in playlist:
            if int(sid) == i['songs_id']:
                song_exist = True
    if song_exist == False:
        playlist.append({'songs_id': int(sid), 'singername': song.singername, 'songname': song.songname})
    request.session['playlist'] = playlist

    if song.songlyrics != '暂无歌词':
        f = open('static/songs-lyrics/' + song.songlyrics, 'r', encoding='utf-8')
        songlyrics = f.read()
        f.close()

    # 收藏
    user = request.session.get('musicuser', [])

    if user:
        try:
            cltmusic_list = cltmusic.objects.get(cltmusic_user_id=user['users_id'], cltmusic_song_id=sid)
            request.session['clt_id'] = 1
        except Exception as error:
            print(error)
            request.session['clt_id'] = 0

    # 评论
    comment_list = comment.objects.filter(commentsong_id=sid).order_by('-commentdate').all()

    if request.method == 'POST':
        ob = comment()
        ob.commenttext = request.POST['commenttext']
        user = request.session.get('musicuser', [])
        if user:
            u = users.objects.get(users_id=user['users_id'])
        ob.commentuser = u
        s = songs.objects.get(songs_id=sid)
        ob.commentsong = s
        ob.save()

    dynamic_info = dynamic.objects.filter(song_id=sid).first()
    if dynamic_info:
        dynamic_info.plays += 1
        dynamic_info.save()
    else:
        dynamic_info = dynamic(plays=1, search=0, down=0, song_id=sid)
        dynamic_info.save()
    return render(request, 'musicplayer.html', locals())


# 歌曲下载
def download(request, sid):
    song_info = songs.objects.get(songs_id=int(sid))
    dynamic_info = dynamic.objects.filter(song_id=int(sid)).first()
    if dynamic_info:
        dynamic_info.down += 1
        dynamic_info.save()
    else:
        dynamic_info = dynamic(plays=0, search=0, down=1, song_id=sid)
        dynamic_info.save()
    file = 'static/songs/' + song_info.filename

    def file_iterator(file, chunk_size=512):
        with open(file, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    filename = song_info.filename
    response = StreamingHttpResponse(file_iterator(file))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(escape_uri_path(filename))
    return response


# 删除当前用户的评论
def deletecomment(request, cid):
    try:
        request.session['musicplayer_from'] = request.META.get('HTTP_REFERER', '/')
        ob = comment.objects.filter(comment_id=cid).delete()
        return HttpResponseRedirect(request.session['musicplayer_from'])
    except Exception as error:
        return HttpResponseRedirect(request.session['musicplayer_from'])


# 添加当前歌曲到用户的收藏
@csrf_exempt
def musiccollect(request, sid):
    clt_id = request.session.get('clt_id', [])
    print(clt_id)
    if clt_id == 0:
        ob = cltmusic()
        user = request.session.get('musicuser', [])
        u = users.objects.get(users_id=user['users_id'])
        ob.cltmusic_user = u
        s = songs.objects.get(songs_id=sid)
        ob.cltmusic_song = s
        ob.save()
        request.session['clt_id'] = 1
    elif clt_id == 1:
        user = request.session.get('musicuser', [])
        ob = cltmusic.objects.get(cltmusic_user_id=user['users_id'], cltmusic_song_id=sid).delete()
        request.session['clt_id'] = 0
    return musicplayer(request, sid)

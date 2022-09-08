from django.urls import path, include
from index.views import index
from index.views import rank
from index.views import singer
from index.views import song
from index.views import search

from haystack.views import SearchView

urlpatterns = [
    path('', index.nevindex,name='nevindex'),
    path('<int:pindex>', index.index,name='index'),
    # 新歌首发
    path('new/<int:pindex>', index.new,name='new'),
    path('inland/<int:pindex>', index.inland,name='inland'),
    path('rthk/<int:pindex>', index.rthk,name='rthk'),
    path('europe/<int:pindex>', index.europe, name='europe'),
    path('korea/<int:pindex>', index.korea, name='korea'),
    path('japanese/<int:pindex>', index.japanese, name='japanese'),
    # 排行榜
    path('rank', rank.rank, name='rank'),
    path('rankinfo/<int:pindex>', rank.rankinfo, name='rankinfo'),
    # 歌手
    path('singer/<int:pindex>',singer.singer,name='singer'),
    path('singerinfo/<int:sid>',singer.singerinfo,name='singerinfo'),
    path('cltsingers/<int:sid>',singer.cltsingers, name='cltsingers'),
    # 歌手
    path('song<int:pindex>', song.song,  name='song'),
    # 搜索
    # path('search', include('haystack.urls')),
    path('search', search.MySearchView(), name='search'),
]
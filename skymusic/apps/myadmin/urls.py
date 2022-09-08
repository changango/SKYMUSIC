from django.urls import path

from myadmin.views import index
from myadmin.views import user
from myadmin.views import song
from myadmin.views import singer
from myadmin.views import dynamic
from myadmin.views import singerssort
from myadmin.views import songssort

urlpatterns = [
    path('',index.index,name='myadmin_index'),
    # 管理员登录
    path('login',index.login,name='myadmin_login'),
    path('dologin',index.dologin,name='myadmin_dologin'),
    path('logout',index.logout,name='myadmin_logout'),
    # 验证码生成
    path('verificationcode', index.verificationcode, name='verificationcode'),
    # 用户管理
    path('user/<int:pindex>', user.index, name='myadmin_user_index'),
    path('user/add', user.add, name='myadmin_user_add'),
    path('user/insert', user.insert, name='myadmin_user_insert'),
    path('user/delete/<int:uid>', user.delete, name='myadmin_user_delete'),
    path('user/edit/<int:uid>', user.edit, name='myadmin_user_edit'),
    path('user/update/<int:uid>', user.update, name='myadmin_user_update'),
    # 歌曲管理
    path('song/<int:pindex>', song.index, name='myadmin_song_index'),
    path('song/add/<int:sid>', song.add, name='myadmin_song_add'),
    path('song/insert/<int:sid>', song.insert, name='myadmin_song_insert'),
    path('song/delete/<int:uid>', song.delete, name='myadmin_song_delete'),
    path('song/edit/<int:uid>', song.edit, name='myadmin_song_edit'),
    path('song/update/<int:uid>', song.update, name='myadmin_song_update'),
    # 歌手管理
    path('singer/<int:pindex>', singer.index, name='myadmin_singer_index'),
    path('singer/add', singer.add, name='myadmin_singer_add'),
    path('singer/insert', singer.insert, name='myadmin_singer_insert'),
    path('singer/delete/<int:uid>', singer.delete, name='myadmin_singer_delete'),
    path('singer/edit/<int:uid>', singer.edit, name='myadmin_singer_edit'),
    path('singer/update/<int:uid>', singer.update, name='myadmin_singer_update'),
    # 歌手歌曲列表
    path('singer/singerinfo/<int:sid>', singer.singerinfo, name='myadmin_singerinfo'),
    # 排行榜管理
    path('dynamic/<int:pindex>', dynamic.index, name='myadmin_dynamic_index'),
    path('dynamic/playsrank/<int:pindex>', dynamic.playsrank, name='myadmin_dynamic_playsrank'),
    path('dynamic/searchrank/<int:pindex>', dynamic.searchrank, name='myadmin_dynamic_searchrank'),
    path('dynamic/downrank/<int:pindex>', dynamic.downrank, name='myadmin_dynamic_downrank'),
    path('dynamic/editrank/<int:uid>',dynamic.editrank,name='myadmin_dynamic_editrank'),
    path('dynamic/updaterank/<int:uid>',dynamic.updaterank,name='myadmin_dynamic_updaterank'),
    # 歌手分类管理
    path('singerssort/<int:pindex>',singerssort.index,name='myadmin_singerssort_index'),
    path('singerssort/add', singerssort.add, name='myadmin_singerssort_add'),
    path('singerssort/insert', singerssort.insert, name='myadmin_singerssort_insert'),
    path('singerssort/delete/<int:uid>', singerssort.delete, name='myadmin_singerssort_delete'),
    path('singerssort/edit/<int:uid>', singerssort.edit, name='myadmin_singerssort_edit'),
    path('singerssort/update/<int:uid>', singerssort.update, name='myadmin_singerssort_update'),
    # 歌曲分类管理
    path('songssort/<int:pindex>',songssort.index,name='myadmin_songssort_index'),
    path('songssort/add', songssort.add, name='myadmin_songssort_add'),
    path('songssort/insert', songssort.insert, name='myadmin_songssort_insert'),
    path('songssort/delete/<int:uid>', songssort.delete, name='myadmin_songssort_delete'),
    path('songssort/edit/<int:uid>', songssort.edit, name='myadmin_songssort_edit'),
    path('songssort/update/<int:uid>', songssort.update, name='myadmin_songssort_update'),
]

from django.urls import path, include

from user import views


urlpatterns = [
    path('login', views.login,name='login'),
    path('dologin', views.dologin,name='dologin'),
    path('logout', views.logout,name='logout'),
    path('enroll', views.enroll,name='enroll'),
    path('doenroll', views.doenroll,name='doenroll'),
    # 验证码
    path('verifcode', views.verifcode, name='verifcode'),
    # 用户主页
    path('myuser', views.myuser, name='myuser'),
    path('parcomment', views.parcomment, name='parcomment'),
    path('parsinger', views.parsinger, name='parsinger'),
    # 用户信息修改
    path('useredit/<int:uid>', views.useredit ,name='useredit'),
    path('douseredit/<int:uid>', views.douseredit ,name='douseredit'),
    # 音乐人
    path('musicsingerindex/<int:uid>', views.musicsingerindex, name='musicsingerindex'),
    path('musicsinger/<int:uid>', views.musicsinger, name='musicsinger'),
    path('musicsingersong/<int:uid>', views.music_upload, name='musicsingersong'),
    path('musicsingerinfo/<int:uid>', views.musicsingerinfo, name='musicsingerinfo'),
    # 好友
    path('friend/<int:uid>', views.friend, name='friend'),
    path('attention/<int:uid>', views.attention, name='attention'),
    path('fans/<int:uid>', views.fans, name='fans'),
    path('del_friend/<int:uid>', views.del_friend, name='del_friend'),
    path('del_attention/<int:uid>', views.del_attention, name='del_attention'),
    path('add_friend/<int:uid>', views.add_friend, name='add_friend')
]
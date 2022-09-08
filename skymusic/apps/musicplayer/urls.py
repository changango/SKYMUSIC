from django.urls import path

from musicplayer import views

urlpatterns = [
    # 用户管理
    path('musicplayer/<int:sid>', views.musicplayer, name='musicplayer'),
    path('download/<int:sid>',views.download, name='download'),
    path('comment/<int:cid>' ,views.deletecomment, name='deletecomment'),
    path('musiccollect/<int:sid>' ,views.musiccollect, name='musiccollect'),

]

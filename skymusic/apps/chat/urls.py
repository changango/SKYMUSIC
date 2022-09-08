from django.urls import path, include
from rest_framework.routers import DefaultRouter

from chat import views
from chat.api import MessageModelViewSet, UsersModelViewSet, UserFriendModelSerializer
from chat.serializers import UserFriendDataModelSerializer

router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UsersModelViewSet, basename='user-api')
router.register(r'friend', UserFriendModelSerializer, basename='friend-api')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('', views.chat, name='chat'),
    path('usersearch/<int:pindex>', views.usersearch, name='usersearch'),
    path('add_user_friend/<int:uid>', views.add_user_friend, name='add_user_friend'),
]

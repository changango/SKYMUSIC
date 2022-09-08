from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from index.models import users, friends
from skymusic import settings
from chat.serializers import MessageModelSerializer, UserModelSerializer, UserFriendModelSerializer
from chat.models import MessageModel


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        user1 = request.session.get('musicuser', [])
        user = users.objects.get(users_id=user1['users_id'])
        self.queryset = self.queryset.filter(Q(recipient=user) |
                                             Q(user=user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=user, user__username=target) |
                Q(recipient__username=target, user=user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user1 = request.session.get('musicuser', [])
        user = users.objects.get(users_id=user1['users_id'])
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=user) |
                                 Q(user=user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class UsersModelViewSet(ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        user = request.session.get('musicuser', [])
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(username=target))
        return super(UsersModelViewSet, self).list(request, *args, **kwargs)


class UserFriendModelSerializer(ModelViewSet):
    queryset = friends.objects.all()
    serializer_class = UserFriendModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None

    def list(self, request, *args, **kwargs):
        user = request.session.get('musicuser', [])
        my_user_id = user['users_id']
        self.queryset = self.queryset.filter(Q(Q(friend_user1_id=my_user_id)&Q(friend_user1_status=1)&Q(friend_user2_status=1))|
                                             Q(Q(friend_user2_id=my_user_id)&Q(friend_user1_status=1)&Q(friend_user2_status=1)))
        return super(UserFriendModelSerializer, self).list(request, *args, **kwargs)
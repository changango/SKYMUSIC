from django.db.models import DateTimeField
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from chat.models import MessageModel
from rest_framework.serializers import ModelSerializer, CharField

from index.models import users, friends


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')
    timestamp = serializers.DateTimeField(format='%Y年%m月%d日 %H:%M', read_only=True)

    def create(self, validated_data):
        user1 = self.context['request'].session.get('musicuser', [])
        user = users.objects.get(users_id=user1['users_id'])

        print(user)
        print(validated_data)
        recipient = get_object_or_404(
            users, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = users
        fields = ('username', 'nickname', 'headprotrait', 'is_status',)


class UserFriendDataModelSerializer(ModelSerializer):
    class Meta:
        model = users
        fields = ('username', 'nickname', 'headprotrait', 'is_status',)


class UserFriendModelSerializer(ModelSerializer):
    # friend_user1 = CharField(source='friend_user1.username', read_only=True)
    friend_user1 = UserFriendDataModelSerializer(many=False)
    friend_user2 = UserFriendDataModelSerializer(many=False)

    class Meta:
        model = friends
        fields = "__all__"

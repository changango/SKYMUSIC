from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json

from index.models import users


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(1)
        user_id = self.scope['url_route']['kwargs']['chat_room']
        # print(user_id)
        update_user_status = await database_sync_to_async(users.objects.get)(users_id=user_id)
        update_user_status.is_status = 'online'
        await database_sync_to_async(update_user_status.save)()
        self.group_name = "{}".format(user_id)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        update_user_status = await database_sync_to_async(users.objects.get)(users_id=self.group_name)
        update_user_status.is_status = 'offline'
        await database_sync_to_async(update_user_status.save)()
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message
            }
        )

    async def recieve_group_message(self, event):
        message = event['message']
        await self.send(
            text_data=json.dumps({
                'message': message
            }))

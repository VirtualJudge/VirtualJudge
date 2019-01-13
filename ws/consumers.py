import json

from channels.generic.websocket import AsyncWebsocketConsumer

from VirtualJudge import settings


class ChatAdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.number = self.scope['url_route']['kwargs']['number']
        self.chat_type = self.scope['url_route']['kwargs']['chat_type']
        self.secret_key = self.scope['url_route']['kwargs']['secret_key']
        self.room_group_name = 'chat_%s_%s' % (self.chat_type, self.number)

        # Join room group
        if str(self.secret_key) == str(settings.SECRET_KEY):
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.number = self.scope['url_route']['kwargs']['number']
        self.chat_type = self.scope['url_route']['kwargs']['chat_type']
        self.room_group_name = 'chat_%s_%s' % (self.chat_type, self.number)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # print(self.scope['user'])
        pass
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']
        #
        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

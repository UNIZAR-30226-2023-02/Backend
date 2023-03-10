import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


# Video iniciacion websockets: https://www.youtube.com/watch?v=cw8-KFVXpTE
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #print(self.scope['url_route']['kwargs'])
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        print(self.room_name)
        #self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
   

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))
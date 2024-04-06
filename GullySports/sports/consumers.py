from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class EchoConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, event):
        self.room_name = "Huzaifa"
        self.room_group_name = "Test_group"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

from channels.consumer import SyncConsumer
from asgiref.sync import async_to_sync

class EchoConsumer(SyncConsumer):

    def websocket_connect(self, event):
        self.room_name = "Huzaifa"
        self.room_group_name= "Test_group"
        async_to_sync(self.channel_layer.group_add)(
            self.send(self.room_name, self.room_group_name)
        )
        self.accept()

    def websocket_receive(self, event):
        self.send({
            "type": "websocket.send",
            "text": event["text"],
        })  
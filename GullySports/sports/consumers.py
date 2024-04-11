import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Match, Team
import json

class CricketMatchDetails(AsyncWebsocketConsumer):
    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        match_details = await self.get_match_details()
        self.room_name = f"match_{self.match_id}"  # Room name
        self.room_group_name = f"live_score_match_{self.match_id}"  

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        match_details_json = json.dumps(match_details)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_match_details',
                'message': match_details_json
            }
        )

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    @sync_to_async
    def get_match_details(self):
        match_details = Match.objects.filter(match_id=self.match_id).values('team_a', 'team_b').first()
        
        print(Team.objects.filter(team_id=match_details['team_a']).values('team_name').first())
        if match_details:
            return {
                'team_a': match_details['team_a'],
                'team_b': match_details['team_b']
            }
        else:
            return None

    async def send_match_details(self, event):
        match_details_json = event['message']
        await self.send(text_data=f"Match Details: {match_details_json}")
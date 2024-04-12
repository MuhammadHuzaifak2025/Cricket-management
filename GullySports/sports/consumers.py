import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Match, Team, Innings
import json

class CricketMatchDetails(AsyncWebsocketConsumer):

    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['role']['match_id']
        if(self.role == "watch")_: # If the role is watch, then the user is a viewer
            self.room_name = f"watch_match{self.match_id}"
            self.room_group_name = f"watch_live_score_match_{self.match_id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        elif(self.role == "update"):
            self.room_name = f"update_match_{self.match_id}"
            self.room_group_name = f"update_live_score_match_{self.match_id}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

        await self.accept()
        match_details = await self.get_match_details()
        if match_details:
            await self.send_match_details({
                'message': match_details
            })
            
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def send_match_details(self, event):
        match_details_json = event['message']
        await self.send(text_data=f"Match Details: {match_details_json}")

    @sync_to_async
    def get_match_details(self):
        match_details = Match.objects.filter(match_id=self.match_id).values('team_a', 'team_b').first()
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

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('Type')
            if message_type == 'update_score':
                print('Innings created')
                await self.update_score(text_data_json)
            elif message_type == 'Start_Innings_01':
                match_id = text_data_json.get('Match_id')
                JD = json.dumps({"match_id":f"{match_id}"})
                print()
                await self.send(JD)
                Innings.objects.create(match_id=text_data_json.get('match_id'), bowling_team=text_data_json.get('bowling_team'), batting_team=text_data_json.get('batting_team'))
                await self.update_match(text_data_json)
        except:
            pass

    async def start_innings(self, data):
        
        pass
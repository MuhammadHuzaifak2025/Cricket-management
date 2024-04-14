import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Match, Team, Innings
import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

# Request Imput Formats at the bottom of the page , search for " # Formats"

class CricketMatchDetails(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            self.match_id = self.scope['url_route']['kwargs']['match_id']
        except KeyError:
            print("KeyError")
            if(self.match_id == None):
                print("Match ID not found")
                await self.close()  
                await self.disconnect(1000)  
        self.room_name = f"watch_match{self.match_id}"
        self.room_group_name = f"watch_live_score_match_{self.match_id}"
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
        else:
           await self.send_match_details({
            'message': "Match not started yet"
        })
           await self.disconnect(self,1000)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
            )
        self.disconnect(1000)
  
    async def send_msg(self, event):
       await self.send(text_data=json.dumps(event['text']))

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


    async def receive(self, text_data):
        try:
            text_data_json =json.loads(text_data)
            message_type = text_data_json.get('Type')
            if message_type == 'Start_Innings_01':
                data = {}
                data = await self.start_innings(text_data_json)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'send_msg',
                        'text': data
                    }
                    )
            elif message_type == 'Start_Innings_02':
                pass
                # match_id = text_data_json.get('Match_id')
                # JD = json.dumps({"match_id":f"{match_id}"})
                # print()
                # await self.send(JD)
                # Innings.objects.create(match_id=text_data_json.get('match_id'), bowling_team=text_data_json.get('bowling_team'), batting_team=text_data_json.get('batting_team'))
                # await self.update_match(text_data_json)
        except:
            pass
    
    @database_sync_to_async
    def start_innings(self, data):
        try:
            match_id = self.match_id
            Innings_01 = Match.objects.filter(match_id=match_id).values('Innings_01').first()
            print(Innings_01)
            if (data.get('batting_team') is None or data.get('bowling_team') is None) or( data.get('batting_team') == data.get('bowling_team')):
                return {
                    "Error": "Invalid team selection"
                }
            BatT = Team.objects.filter(team_id=data.get('batting_team')).first()
            BallT = Team.objects.filter(team_id=data.get('bowling_team')).first()
            innings_details = {
                        'status': '',
                        'batting_team': BatT.team_name,
                        'bowling_team': BallT.team_name,
                        'extras': 0,
                        'total': 0,
                        'wickets': 0,
                        "Error" : "Null"
                    }
            if Innings_01 is None or Innings_01.get("Innings_01") is None:

                if BallT and BatT:
                    Innings_1 = Innings.objects.create(bowling_team=BallT, batting_team=BatT)
                    Match.objects.filter(match_id=match_id).update(Innings_01=Innings_1)
                    innings_details['status'] = "Innings_01 Started"
                    return innings_details
                else:
                    innings_details = {
                        "Error": "Team not found"
                    }
                    return innings_details 
            else:
                if Match.objects.filter(match_id=match_id).values('Innings_02').first().get('Innings_02') is not None:
                    innings_details['Error'] = "Innings already started"
                    return innings_details
                innings_details = Innings.objects.filter(innings_id=Innings_01["Innings_01"]).values('batting_team', 'bowling_team', 'extras', 'total', 'wickets').first()
                Innings2 = Innings.objects.create(bowling_team=BallT, batting_team=BatT)
                Match.objects.filter(match_id=match_id).update(Innings_02=Innings2)
                innings_details['Errors'] = "Null"
                innings_details['status'] = "Innings_02 Started"
                if innings_details:
                    return innings_details
                    # self.send_Innings_01(innings_details)


                    # print("Sending innings details0")
                else:
                    print("Innings details not found")
            # This line creates another innings object, it might not be necessary
            # Innings.objects.create(match_id=match_id, bowling_team=data.get('bowling_team'), batting_team=data.get('batting_team'))

        except Match.DoesNotExist:
            print("Match not found")
        except Exception as e:
            print("Error:", e)

# Formats
# {
#     "Type": "Start_Innings_01",
#     "batting_team":15,
#     "bowling_team":16
# }

from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Innings, Player, Team, Match, BallEvent, Coach
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from faker import Faker
import datetime

@api_view(http_method_names=['POST'])
def Create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    if not User.objects.filter(username=username):
        User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({"User":"created"})
    
    return JsonResponse({"User":"exsist"})

@api_view(http_method_names=['POST'])
def NewPlayer(request):
    Gender = None
    PlayerName = request.data.get('PlayerName')
    Age = request.data.get('Age')
    Genders = request.data.get('Genders')
    Password = request.data.get('Password')
    Salary = request.data.get('Salary')

    user = User.objects.filter(username = PlayerName).values('username')
    print(user.count())
    if(user.count() ==0):    
        if(Genders):
            Gender = True
        else: Gender = False
        User.objects.create(username = PlayerName, password = Password)
        Players = Player.objects.create(name = PlayerName,age = Age, salary = Salary, gender = Gender)
        if(Players):
            return JsonResponse({"Status":"Created Player"}, status = 200)
        else: return JsonResponse({"Status":"Error Creating Player"}, status = 400)
    else:
         return JsonResponse({"Status":"Player Already Registered"}, status = 400)
@api_view(http_method_names=['GET'])
def temp():
    return JsonResponse({"asd":"sad"})

from rest_framework.authtoken.models import Token
@api_view(http_method_names=['POST'])
def LoginUser(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        user = authenticate(request, username=username, password=password)
        session_id = request.session.session_key
        if session_id is None:
            session_id = request.session.create()
        if user is not None:
            # created = Token.objects.get_or_create(user=user)
            return JsonResponse({"User": "Login Success", "Token": f"{session_id}"})
        else:
            return JsonResponse({"User": "Login Failed"})
    else:
        return JsonResponse({"User": "User not found"})
    
@api_view(http_method_names=['GET'])
def getPlayerdata(request, playername=None):
    if request.user.is_authenticated or playername is not None:
        user = request.user
        if playername is not None:
            user = User.objects.filter(username=playername)[0]
        player = Player.objects.filter(user=user)
        print(player)
        if player.exists():
            player_recs = Player.objects.filter(name=player.values('name')[0].get('name')).values('name', 'age', 'salary')
            ballEvents = BallEvent.objects.filter(batsman__name=player[0]).values('type', 'score')

            total_score = 0
            wickets = 0
            for event in ballEvents:
                total_score += event['score']
                if event['type'] == 'wicket':
                    wickets += 1

            if ballEvents.exists():
                # print(BallEvent[0].get('score').count())
                return JsonResponse({"Player": player_recs[0], "Total Score": total_score, "Wickets": wickets, "Avg": total_score/ballEvents.count()})
            else:
                return JsonResponse({"Player": "No Data Found"})
        else:
            return JsonResponse({"Player": "Player name not provided"})
    else:
        return JsonResponse({"Player": "Not Logged In"})


@api_view(http_method_names=['GET'])
def getTeamData(request, teamname):
    if request.user.is_anonymous:
        return JsonResponse({"Response": "Not Logged In"},status = 400)
    team = Team.objects.filter(team_name=teamname)
    if team.exists():
        team_recs = team.values('team_name', 'coaches', 'players')
        players = Player.objects.filter(team=team[0]).values('name', 'age', 'salary')
        if players.exists():
            return JsonResponse({"Team": team_recs[0], "Players": list(players), "Count":f'{players.count()}'})
        else:
            return JsonResponse({"Team": "No Players Found"})
    return JsonResponse({"Team": "Team not found"})

@api_view(http_method_names=['POST'])
def NewCoach(request):
    CoachName = request.data.get('CoachName')
    Age = request.data.get('Age')
    Salary = request.data.get('Salary')
    Password = request.data.get('Password')

    user = User.objects.filter(username = CoachName).values('username')
    if(user.count() == 0):    
        if Password is None or len(Password) == 0:
            return JsonResponse({"Status":"Password Required"}, status = 400)
        User.objects.create(username = CoachName, password = Password)
        
        Coaches = Coach.objects.create(name = CoachName,age = Age, salary = Salary)
        if(Coaches):
            return JsonResponse({"Status":"Created Coach"}, status = 200)
        else: return JsonResponse({"Status":"Error Creating Coach"}, status = 400)
    else:
         return JsonResponse({"Status":"Coach Already Registered"}, status = 400)

@api_view(http_method_names=['POST'])
def NewTeam(request,TeamName):
    if(Team.objects.filter(team_name = TeamName).count() == 0):
        Teams = Team.objects.create(team_name = TeamName)
        return JsonResponse({"Status":"Created Team"}, status = 200)
    return JsonResponse({"Status":"Team with samename cant be created"}, status = 400)

@api_view(http_method_names=['POST'])
def AddPlayerToTeam(request, TeamName, PlayerName):
    Inp_Team = Team.objects.filter(team_name = TeamName)
    Inp_Players = Player.objects.filter(name = PlayerName)
    if(Inp_Team.count() == 0):
        if(Inp_Players.count() == 0):
            return JsonResponse({"Status":"Player Not Found"}, status = 400)
        Inp_Team.players.add(Inp_Players[0])
        return JsonResponse({"Status":"Player Added to Team"}, status = 200)
    return JsonResponse({"Status":"Team Not Found"}, status = 400)

# user = User.objects.filter(username = PlayerName).values('username')
#     print(user.count())
#     if(user.count() ==0):    
#         if(Genders):
#             Gender = True
#         else: Gender = False
#         User.objects.create(username = PlayerName, password = Password)
#         Players = Player.objects.create(name = PlayerName,age = Age, salary = Salary, gender = Gender)
#         if(Players):
#             return JsonResponse({"Status":"Created Player"}, status = 200)


def temp_generate_teams(request):
    fake = Faker()
    TeamName = fake.name()
    team = Team.objects.create(team_name=TeamName)
    for i in range(0,11):
        name = fake.name()
        passw = fake.password()
        NewPlayer(request=request, PlayerName=name, Age=fake.random_int(min=18, max=40),Password = passw,Genders = fake.random_int(min=0, max=1),Salary=fake.random_int(min=10000, max=100000) )
        user = User.objects.filter(username = name).values('username')
        if(user.count() ==0):    
            if(fake.random_int(min=0, max=1) == 1):
                Gender = True
            else: Gender = False
            User.objects.create(username = name, password = passw)
            Players = Player.objects.create(name = name,age = fake.random_int(min=18, max=40), salary = fake.random_int(min=10000, max=100000), gender = Gender)
        else:
            Players = Player.objects.filter(name=name)[0]
        team.players.add(Players)
    return JsonResponse({"Status": f'Teams Created with name {TeamName}. '})
from datetime import date

@api_view(http_method_names=['POST'])
def create_match(request):
    Team2Name = request.data.get('Team2Name')
    Team1Name = request.data.get('Team1Name')
    Venue = request.data.get('Venue')


    if(Team2Name == Team1Name):
        return JsonResponse({"Status": "Both Teams can't be same"},status = 400)
    team1 =Team.objects.filter(team_name=Team1Name) 
    team2 =Team.objects.filter(team_name=Team2Name) 
    if team1.count()== 0:
        return JsonResponse({"Status": f"{Team1Name} not found"},status = 400)
    if team2.count() == 0:
        return JsonResponse({"Status": f"{Team2Name} not found"},status = 400)
    Team_a = Match.objects.filter(team_a = team1[0],date =datetime.datetime.now())
    Team_b = Match.objects.filter(team_b = team2[0],date =datetime.datetime.now())
    if(Team_a.count() > 0 and Team_b.count() > 0):
        return JsonResponse({"Status": f"Both Teams {Team1Name} and {Team2Name} are already playing a match on date: {datetime.datetime.now()}"},status = 400)
    if Team_a.count() > 0:
        return JsonResponse({"Status": f"{Team1Name} is already playing a match on date: {datetime.datetime.now().date()}"},status = 400)
    if Team_b.count() > 0: 
        return JsonResponse({"Status": f"{Team2Name} is already playing a match on date: {datetime.datetime.now().date()}"},status = 400) 

    if request.user.is_authenticated:
        if request.user.is_staff :
            match = Match.objects.create(team_a=team1[0], team_b=team2[0], venue= Venue)
            return JsonResponse({"Status": "Match Created"})
        else:
            return JsonResponse({"Status": "Not Authorized to create match"})
    else:
        return JsonResponse({"Status": "Not Logged In"})
    
@api_view(http_method_names=['GET'])
def view_all_matches(request):
    matches = Match.objects.all()
    matches_list = []
    for match in matches:
        matches_list.append({
            'team_a': match.team_a.team_name,
            'team_b': match.team_b.team_name,
            'venue': match.venue,
            'date': match.date,
            'match_id': match.match_id
        })
    return JsonResponse({"Matches": matches_list})
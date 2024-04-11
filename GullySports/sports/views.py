from django.shortcuts import render
from .models import Innings, Player, Team, Match, BallEvent, Coach
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from faker import Faker
import datetime


def Create_user(request, username=None, email=None, password=None):
    username = "Huzaifa_Ali3"
    password = "check"
    email = None
    if not User.objects.filter(username=username):
        User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({"User":"created"})
    return JsonResponse({"User":"exsist"})

def NewPlayer(request, PlayerName, Age, Genders, Password, Salary=None):
    Gender = None
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
def temp():
    return JsonResponse({"asd":"sad"})

def LoginUser(request, username=None, password=None):
    if User.objects.filter(username=username).exists():
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return JsonResponse({"User": "Login Success"})
        else:
            return JsonResponse({"User": "Login Failed"})
    else:
        return JsonResponse({"User": "User not found"})
        
def getPlayerdata(request, playername=None):
    if request.user.is_authenticated:
        user = request.user
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


#   Not Working  
# def getmyTeamData(request, teamname=None):
#     if User.is_authenticated:
#         user = User.objects.filter(username=User.username)
#         print(user)
#         team = Team.objects.filter(players=user[0])
#         print(team)
#         if team.exists():
#             team_recs = Team.objects.filter(name=team.values('name')[0].get('name')).values('name', 'coach', 'captain')
#             players = Player.objects.filter(team=team[0]).values('name', 'age', 'salary')

#             if players.exists():
#                 return JsonResponse({"Team": team_recs[0], "Players": list(players)})
#             else:
#                 return JsonResponse({"Team": "No Players Found"})
#         else:
#             return JsonResponse({"Team": "Team name not provided"})
#     else:
#         return JsonResponse({"Team": "Not Logged In"})

def NewCoach(request, CoachName,Password ,Age, Salary):

    user = User.objects.filter(username = CoachName).values('username')
    if(user.count() == 0):    
        User.objects.create(username = CoachName, password = Password)
        
        Coaches = Coach.objects.create(name = CoachName,age = Age, salary = Salary)
        if(Coaches):
            return JsonResponse({"Status":"Created Coach"}, status = 200)
        else: return JsonResponse({"Status":"Error Creating Coach"}, status = 400)
    else:
         return JsonResponse({"Status":"Coach Already Registered"}, status = 400)

def NewTeam(request,TeamName):
    if(Team.objects.filter(team_name = TeamName).count() == 0):
        Teams = Team.objects.create(team_name = TeamName)
        return JsonResponse({"Status":"Created Team"}, status = 200)
    return JsonResponse({"Status":"Team with samename cant be created"}, status = 400)

def AddPlayerToTeam(request, TeamName, PlayerName):
    if(Team.objects.filter(team_name = TeamName).count() == 0):
        Teams = Team.objects.filter(team_name = TeamName)
        if(Player.objects.filter(name = PlayerName).count() == 0):
            return JsonResponse({"Status":"Player Not Found"}, status = 400)
        Players = Player.objects.filter(name = PlayerName)
        Teams.players.add(Players[0])
        return JsonResponse({"Status":"Player Added to Team"}, status = 200)
    return JsonResponse({"Status":"Team Not Found"}, status = 400)

def temp_generate_teams(request):
    fake = Faker()
    
    TeamName = fake.name()
    team = Team.objects.create(team_name=TeamName)
    for i in range(0,11):
        name = fake.name()
        passw = fake.password()
        NewPlayer(request=request, PlayerName=name, Age=fake.random_int(min=18, max=40),Password = passw,Genders = fake.random_int(min=0, max=1),Salary=fake.random_int(min=10000, max=100000) )    
        team.players.add(Player.objects.filter(name=name)[0])
    return JsonResponse({"Status": f'Teams Created with name {TeamName}. '})


def create_match(request, Team2Name, Team1Name, Venue=None, date=None, time=None):
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
        return JsonResponse({"Status": f"Both Teams {Team1Name} and {Team2Name} are already playing a match"},status = 400)
    if Team_a.count() > 0:
        return JsonResponse({"Status": f"{Team1Name} is already playing a match"},status = 400)
    if Team_b.count() > 0: 
        return JsonResponse({"Status": f"{Team2Name} is already playing a match"},status = 400) 

    if User.is_authenticated:
        if User.is_staff :
            match = Match.objects.create(team_a=team1[0], team_b=team2[0], venue= Venue)
            return JsonResponse({"Status": "Match Created"})
        else:
            return JsonResponse({"Status": "Not Authorized to create match"})
    else:
        return JsonResponse({"Status": "Not Logged In"})
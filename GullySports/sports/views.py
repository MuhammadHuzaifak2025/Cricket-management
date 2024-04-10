from django.shortcuts import render
from .models import Innings, Player, Team, Match, BallEvent, Coach
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse

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
    

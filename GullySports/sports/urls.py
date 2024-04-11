from django.contrib import admin
from django.urls import path, include
from sports import views

urlpatterns = [
    path('api/CreateUser', views.Create_user, name="CreateUser"),
    path('api/NewCoach/<str:CoachName>/<str:Password>/<int:Age>/<int:Salary>/', views.NewCoach, name="NewCoach"),
    path('api/LoginUser/<str:username>/<str:password>', views.LoginUser, name="userlogin"),
    path('api/getPlayerdata', views.getPlayerdata, name="getPlayerdata"),
    # path('api/getmyTeamData', views.getmyTeamData, name="getTeamData"),
    path('temp', views.NewTeam, name="CreateUser"),
    path('api/NewPlayer/<str:PlayerName>/<str:Password>/<int:Age>/<int:Salary>/<int:Genders>/', views.NewPlayer, name="CreateNewPlayer"),
    path('api/NewTeam/<str:TeamName>/', views.NewTeam, name=" CeatedNewTeam"),
    path('api/AddPlayerToTeam/<str:TeamName>/<str:PlayerName>/', views.AddPlayerToTeam, name="AddedPlayerToTeam"),
    path('api/temp/temp_generate_teams', views.temp_generate_teams, name="temp_generate_teams"),
    path('api/create_match/<str:Team1Name>/<str:Team2Name>/<str:Venue>', views.create_match, name="create_match"),
]

from django.contrib import admin
from django.urls import path, include
from sports import views

urlpatterns = [
    path('api/CreateUser', views.Create_user, name="CreateUser"),
    path('api/NewCoach/', views.NewCoach, name="NewCoach"),
    path('api/LoginUser/', views.LoginUser, name="userlogin"),
    path('api/getPlayerdata/<str:playername>/', views.getPlayerdata, name="getPlayerdata"),
    path('api/getPlayerdata/', views.getPlayerdata, name="getPlayerdata"),
    path('api/getmyTeamData/<str:teamname>/', views.getTeamData, name="getTeamData"),
    path('temp', views.NewTeam, name="CreateUser"),
    path('api/NewPlayer/<str:PlayerName>/<str:Password>/<int:Age>/<int:Salary>/<int:Genders>/', views.NewPlayer, name="CreateNewPlayer"),
    path('api/NewTeam/<str:TeamName>/', views.NewTeam, name=" CeatedNewTeam"),
    path('api/AddPlayerToTeam/<str:TeamName>/<str:PlayerName>/', views.AddPlayerToTeam, name="AddedPlayerToTeam"),
    path('api/temp/temp_generate_teams/', views.temp_generate_teams, name="temp_generate_teams"),
    path('api/create_match/', views.create_match, name="create_match"),
    path('api/view_all_matches/', views.view_all_matches, name="view_all_matches"),
    path('api/perform_toss/', views.performtoss, name="performtoss"),
]

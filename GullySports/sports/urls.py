from django.contrib import admin
from django.urls import path, include
from sports import views

urlpatterns = [
    path('api/CreateUser', views.Create_user, name="CreateUser"),
    path('api/LoginUser/<str:username>/<str:password>', views.LoginUser, name="userlogin"),
    path('api/getPlayerdata', views.getPlayerdata, name="getPlayerdata"),
    path('temp', views.temp, name="CreateUser"),
    path('api/NewPlayer/<str:PlayerName>/<str:Password>/<int:Age>/<int:Salary>/<int:Genders>/', views.NewPlayer, name="CreateNewPlayer"),
]

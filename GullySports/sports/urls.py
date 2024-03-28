from django.contrib import admin
from django.urls import path, include
from sports import views

urlpatterns = [
    path('', views.Create_user, name="CreateUser")
]

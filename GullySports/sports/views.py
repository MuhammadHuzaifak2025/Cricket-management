from django.shortcuts import render
from models import *
from django.contrib.auth.models import User,create_user

def Create_user(username, password, email):
    username = "Huzaifa"
    password = "check"
    email = None
    create_user(username, email, password)


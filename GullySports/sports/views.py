from django.shortcuts import render
from .models import Innings
from django.contrib.auth.models import User
from django.http import JsonResponse

def Create_user(request, username=None, email=None, password=None):
    username = "Huzaifa_Ali3"
    password = "check"
    email = None
    if not User.objects.filter(username=username):
        User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({"User":"created"})
    return JsonResponse({"User":"exsist"})
# """
# ASGI config for GullySports project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
# """


import os
from sports.consumers import *

from django.urls import path
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GullySports.settings')

django_asgi_app = get_asgi_application()

ws_pattern = [
    path('ws/live_score/<int:match_id>/', CricketMatchDetails.as_asgi()),
]
application = ProtocolTypeRouter({
    'websocket' : URLRouter(ws_pattern),
    'http' : django_asgi_app 
})
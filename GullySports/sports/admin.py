from django.contrib import admin
from sports.models import Player, BallEvent, Coach, Innings, Team, Match
# Register your models here.
admin.site.register(Player),
admin.site.register(Coach),
admin.site.register(Team),
admin.site.register(Match),
admin.site.register(Innings),
admin.site.register(BallEvent),
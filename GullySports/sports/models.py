from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)   
    player_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return self.name
    
class Coach(models.Model):
    coach_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)
    coaches = models.ManyToManyField(Coach)
    players = models.ManyToManyField(Player)  

    def __str__(self):
        return self.team_name

class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_b')
    venue = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.team_a.team_name} vs {self.team_b.team_name}"
    
class BallEvent(models.Model):
    ball_event_id = models.AutoField(primary_key=True, auto_created=True)
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowler')
    batsman = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batsman')
    type = models.CharField(max_length=50)
    score = models.IntegerField()

    def __str__(self):
        return f"Ball {self.ball_event_id}"

class Innings(models.Model):
    innings_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    batting_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_team')
    bowling_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='bowling_team')
    ball_events = models.ManyToManyField(BallEvent)

    def __str__(self):
        return f"Innings {self.id} - {self.match}"
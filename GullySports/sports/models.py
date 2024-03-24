from django.db import models


# class Player(models.Model):
#     Genders = {
#         "M" : "Male",
#         "F" : "Female",
#         "O" : "Others",

#     }
#     Playerid = models.AutoField(primary_key=True, auto_created=True)
#     Name = models.CharField(max_length=300)
#     Dateofbirth = models.DateField()
#     Age = models.IntegerField()
#     Gender = models.TextChoices(choices=Genders,max_length=1)
    
# from django.db import models

class Player(models.Model):
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
    ball_event_id = models.AutoField(primary_key=True)
    # innings = models.ForeignKey(Innings, on_delete=models.CASCADE)
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowler')
    batsman = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batsman')
    # You can expand this model to include details about the ball type (run, wicket, etc.), score, etc.
    type = models.CharField(max_length=50)
    score = models.IntegerField()

    def __str__(self):
        return f"Ball {self.id} - {self.innings}"

class Innings(models.Model):
    innings_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    batting_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_team')
    bowling_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='bowling_team')
    ball_events = models.ManyToManyField(BallEvent)

    def __str__(self):
        return f"Innings {self.id} - {self.match}"


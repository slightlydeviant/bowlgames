from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# hard coded section:
currentseason = '2014'
champgame = 'CFP National Championship' # must match game title in both database and url
url = 'http://scores.espn.go.com/ncf/scoreboard?confId=80&seasonYear=2014&seasonType=3&weekNumber=17'

# Code first models:
class Game(models.Model):
    game = models.CharField(max_length = 80)
    kickoff_time = models.DateTimeField()
    weight = models.IntegerField(default = 1)
    totalscore = models.IntegerField(null=True, blank=True)
    season = models.CharField(max_length = 80)
    def __unicode__(self):
        return self.game

class Team(models.Model):
    game = models.ForeignKey(Game)
    team = models.CharField(max_length = 80)
    # win = models.NullBooleanField()
    win = models.IntegerField(default = 0)
    display_name = models.CharField(max_length = 2)
    def __unicode__(self):
        return self.team

class UserPicks(models.Model):
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    pick = models.ForeignKey(Team, null=True, blank=True)
    tiebreak = models.IntegerField(null=True, blank=True)
    pick_date = models.DateTimeField(null=True, blank=True)

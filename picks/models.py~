from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# hard coded section:
currentseason = 'Conference Championships'
champgame = 'BCS CHAMPIONSHIP' # must match game title in both database and url
url = 'http://scores.espn.go.com/ncf/scoreboard?seasonYear=2014&seasonType=2&weekNumber=15'

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

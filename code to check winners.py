from picks.models import *
from webscrape import winTeam

for t in Team.objects.all()
    if t.team in winTeam:
        t.win = True

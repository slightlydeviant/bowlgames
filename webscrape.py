# webscrape.py

from bs4 import BeautifulSoup
import requests
import re
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bowlgames.settings')

import bowlgames
from django.contrib.auth.models import User
from picks.models import *

# hard coded section:
url = 'http://scores.espn.go.com/ncf/scoreboard?confId=8&seasonYear=2014&seasonType=2&weekNumber=14'
# champgame = 'Iron Bowl'
#url = 'http://scores.espn.go.com/ncf/scoreboard?seasonYear=2013&seasonType=3&weekNumber=17'
# champgame = 'BCS'

r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

# Find winners and save to database
winTeam = []

games = soup.find_all('div', class_='gameDay-Container')
for game in games:
    winners = game.find_all('div', class_='winner-arrow', style='display:block')
    for team in winners:
        winTeam.append(re.sub(r'^[0-9]+|;', '', team.parent.find('p', class_='team-name').text.strip()))

# for tm in winTeam:
#     print tm

for tm in Team.objects.filter(game__season == currentseason):
    if tm.team in winTeam:
        tm.win = True
        tm.save()

# Get game total scores
# for gm in soup.find_all('div', class_='game-notes'):
#     if 'BCS NATIONAL CHAMPIONSHIP' in gm.text:
#         scores = gm.find_all('li', class_='final')
#         total = int(scores[1]) + int(scores[2])
#         bcschamp = Game.objects.filter(season=currentseason, game__contains=champgame)
#         bcschamp.totalscore = total
#         bcschamp.save()

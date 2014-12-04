from picks.models import *
from webscrape import winTeam

for t in Team.objects.all()
    if t.team in winTeam:
        t.win = True


# cron specification
# MAILTO = "scoob1212@yahoo.com"
# min     hour    day     month   weekday user  file
# */10    12-1    *       12,1    *       web   /home/web/sites/bowlgames_production/cronjob.sh

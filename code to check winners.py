from picks.models import *
from webscrape import winTeam

for t in Team.objects.all()
    if t.team in winTeam:
        t.win = True


# cron specification
# MAILTO = "scoob1212@yahoo.com"
# min     hour    day     month   weekday user  file
# */10    12-1    *       12,1    *       web   /home/web/sites/bowlgames_production/cronjob.sh


true_score = Game.objects.get(game__contains=champgame).totalscore
if true_score is None:
    # regular leaderboard
else:
    # rank code
    firstplacelist = [x for (rank, x) in list(ranks) if rank == 1]

    def breakTie(self):
        return (self,
                abs(self.userpicks_set.get(game__game__contains=champgame).tiebreak - true_score))
    def getBreakTie(self):
        return breakTie(self)[1]
    # display a champion message

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate
from django.db.models import Sum
import datetime
import re
from django.utils import timezone
from ranking import Ranking

from django.contrib.auth.models import User
from picks.models import Game, Team, UserPicks, currentseason

def pickwinners(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('accounts:login_page'))
    # # Close picks after first kickoff
    # if min(Game.objects.filter(season = currentseason)\
    #     .values_list('kickoff_time', flat=True)) < timezone.now():
    #     msg1 = "Too Late!"
    #     msg2 = "The first game has already started. You may no longer change your picks, but you may check them "
    #     return render(request, 'picks/closed.html', {'msg_head': msg1, 'msg_body': msg2})
    else:
        game_list = Game.objects.filter(season=currentseason)
        user_ob = request.user
        context = {'game_list': game_list, 'user_ob': user_ob}
        return render(request, 'picks/gamepicks.html', context)

def savepicks(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('accounts:login_page'))
    else:
        user = request.user
        game_list = Game.objects.filter(season = currentseason).values_list('id', flat=True)
        key_list = list(set(request.POST) & set(map(str, game_list)))

        for key in key_list:
            pick_exists = UserPicks.objects.filter(
                          user = User.objects.filter(username=user),
                          game = key)
            if(pick_exists):
                if(request.POST[key] == ''):
                    continue
                else:
                    pick_exists.update(pick = Team.objects.get(id = request.POST[key]),
                                       tiebreak = request.POST.get(key + '_tiebreak', None),
                                       pick_date = timezone.now())
            else:
                if(request.POST[key] == ''):
                    up = UserPicks(user = User.objects.get(username = user),
                                   tiebreak = request.POST.get(key + '_tiebreak', None),
                                   game = Game.objects.get(id = key))
                    up.save()
                else:
                    up = UserPicks(user = User.objects.get(username = user),
                                   game = Game.objects.get(id = key),
                                   pick = Team.objects.get(id = request.POST[key]),
                                   tiebreak = request.POST.get(key + '_tiebreak', None),
                                   pick_date = timezone.now())
                    up.save()
        allpicks = UserPicks.objects.filter(user = User.objects.filter(username=user),
                                            game__season = currentseason)
        return render(request, 'picks/output.html', {'out_list': key_list, 'allpicks': allpicks})

def pickgrid(request):
    # # Close grid while picks are live (before first kickoff)
    # if min(Game.objects.filter(season = currentseason)\
    #     .values_list('kickoff_time', flat=True)) > timezone.now():
    #     msg1 = "No Peeking!"
    #     msg2 = "Others are still making their picks. You may check your picks "
    #     return render(request, 'picks/closed.html', {'msg_head': msg1, 'msg_body': msg2})
    # else:
        users = User.objects.filter(id__in=UserPicks.objects.filter(game__season = currentseason)\
            .values('user').distinct())
        games = Game.objects.filter(season = currentseason)
        allpicks = UserPicks.objects.filter(game__season = currentseason)
        allpicks2 = UserPicks.objects.filter(game__season = currentseason).order_by('game')
        pointlist = User.objects.filter(userpicks__game__season = currentseason)\
            .annotate(points=Sum('userpicks__pick__win'))

        for person in pointlist:
            if person.points == None:
                person.points = 0

        context = {'users': users, 'games': games, 'allpicks': allpicks,
                   'allpicks2': allpicks2, 'pointlist': pointlist}
        return render(request, 'picks/pickgrid.html', context)

def leader(request):
    currentuser = request.user
    pointlist = User.objects.filter(userpicks__game__season = currentseason)\
        .annotate(points=Sum('userpicks__pick__win'))\
        .order_by('-points', 'first_name')

    for person in pointlist:
        if person.points == None:
            person.points = 0

# insert tiebreaker logic here:
# maybe annotate(Sum(tiebreak), Sum(totalscore))
# diff = abs(tie_sum - total_sum)
# order_by('-points', 'diff', 'first_name')

    def getPoints(self):
        return self.points

    ranks = Ranking(pointlist, start = 1, key = getPoints)
    ranklist = list(ranks)

    # currentrank = ranks.rank(currentuser)

    context = {'pointlist': ranklist, 'currentuser': currentuser}  # , 'currentrank': currentrank}
    return render(request, 'picks/leaderboard.html', context)

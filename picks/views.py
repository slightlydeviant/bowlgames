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
from picks.models import *

def pickwinners(request):
    """Renders the pick selection page. Populates dropdown lists"""
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('accounts:login_page'))
    # Close picks after first kickoff
    if min(Game.objects.filter(season = currentseason)\
        .values_list('kickoff_time', flat=True)) < timezone.now():
        msg1 = "Too Late!"
        msg2 = "The first game has already started. You may no longer change your picks, but you may check them "
        return render(request, 'picks/closed.html', {'msg_head': msg1, 'msg_body': msg2})
    else:
        game_list = Game.objects.filter(season=currentseason)
        user_ob = request.user
        context = {'game_list': game_list, 'user_ob': user_ob}
        return render(request, 'picks/gamepicks.html', context)

def savepicks(request):
    """Saves picks from pick selection page. Renders current picks page"""
    def isInt(num):
        try:
            int(num)
        except ValueError:
            return False
        else:
            if int(num) > 0:
                return True
            else:
                return False

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('accounts:login_page'))
    else:
        user = request.user
        game_list = Game.objects.filter(season = currentseason).values_list('id', flat=True)
        key_list = list(set(request.POST) & set(map(str, game_list)))
        tiebreak_error = False

        for key in key_list:
            pick_exists = UserPicks.objects.filter(
                          user = User.objects.filter(username=user),
                          game = key)

            tiebreaker_pick = request.POST.get(key + '_tiebreak', None)

            if tiebreaker_pick in [None, '']:
                if(pick_exists):
                    if(request.POST[key] == ''):
                        continue
                    else:
                        pick_exists.update(pick = Team.objects.get(id = request.POST[key]),
                                           pick_date = timezone.now())
                else: # if pick does not exist
                    if(request.POST[key] == ''):
                        up = UserPicks(user = User.objects.get(username = user),
                                       game = Game.objects.get(id = key))
                        up.save()
                    else:
                        up = UserPicks(user = User.objects.get(username = user),
                                       game = Game.objects.get(id = key),
                                       pick = Team.objects.get(id = request.POST[key]),
                                       pick_date = timezone.now())
                        up.save()
            else: # tiebreaker pick is not None or '' (blank)
                if isInt(tiebreaker_pick) is False:
                    tiebreak_error = True
                    break
                else:
                    if(pick_exists):
                        if(request.POST[key] == ''):
                            pick_exists.update(tiebreak = int(tiebreaker_pick),
                                               pick_date = timezone.now())
                        else:
                            pick_exists.update(pick = Team.objects.get(id = request.POST[key]),
                                               tiebreak = int(tiebreaker_pick),
                                               pick_date = timezone.now())
                    else: # if pick does not exist
                        if(request.POST[key] == ''):
                            up = UserPicks(user = User.objects.get(username = user),
                                           tiebreak = int(tiebreaker_pick),
                                           game = Game.objects.get(id = key))
                            up.save()
                        else:
                            up = UserPicks(user = User.objects.get(username = user),
                                           game = Game.objects.get(id = key),
                                           pick = Team.objects.get(id = request.POST[key]),
                                           tiebreak = int(tiebreaker_pick),
                                           pick_date = timezone.now())
                            up.save()

        if tiebreak_error:
            game_list = Game.objects.filter(season=currentseason)
            user_ob = request.user
            error_message = 'Your tiebreaker points (' + tiebreaker_pick + ') must be a positive whole number'
            context = {'game_list': game_list, 'user_ob': user_ob, 'error_message': error_message}
            return render(request, 'picks/gamepicks.html', context)
        else:
            allpicks = UserPicks.objects.filter(user = User.objects.filter(username=user),
                                                game__season = currentseason)
            context = {'allpicks': allpicks}  # 'out_list': key_list,
            return render(request, 'picks/output.html', context)

def pickgrid(request):
    """Renders the grid of all picks by all users"""
    # Close grid while picks are live (before first kickoff)
    if min(Game.objects.filter(season = currentseason)\
        .values_list('kickoff_time', flat=True)) > timezone.now():
        msg1 = "No Peeking!"
        msg2 = "Others are still making their picks. You may check your picks "
        return render(request, 'picks/closed.html', {'msg_head': msg1, 'msg_body': msg2})
    else:
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
    """Renders the leaderboard for all users"""
    currentuser = request.user
    pointlist = User.objects.filter(userpicks__game__season = currentseason)\
        .annotate(points=Sum('userpicks__pick__win'))\
        .order_by('-points', 'first_name')

    for person in pointlist:
        if person.points == None:
            person.points = 0

    def getPoints(self):
        return self.points
    def breakTie(self):
        return (abs(self.userpicks_set.get(game__game__contains = champgame).tiebreak - true_score),
                self)
    def getBreakTie(self):
        return breakTie(self)[0]

    true_score = Game.objects.get(game__contains=champgame).totalscore
    if true_score is None:
        ranks = Ranking(pointlist, start = 1, key = getPoints)
        ranklist = list(ranks)
        winner = False
    else:
        ranks = Ranking(pointlist, start = 1, key = getPoints)
        ranklist = list(ranks)

        firstplacelist = [x for (rank, x) in ranklist if rank == 1]

        firstplaceranks = [breakTie(x) for x in firstplacelist]
        firstplaceranks.sort()
        firstplace = firstplaceranks[0]
        pointlist2 = User.objects.filter(userpicks__game__season = currentseason)\
            .exclude(id = firstplace[1].id)\
            .annotate(points=Sum('userpicks__pick__win'))\
            .order_by('-points', 'first_name')
        for person in pointlist2:
            if person.points == None:
                person.points = 0
        therest = Ranking(pointlist2, start = 2, key = getPoints)
        ranklist = list(therest)
        ranklist.insert(0, (1, firstplace[1]))
        winner = firstplace[1].first_name


    context = {'pointlist': ranklist, 'currentuser': currentuser, 'winner': winner}
    return render(request, 'picks/leaderboard.html', context)

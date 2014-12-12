from django.conf.urls import patterns, url
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from picks import views

urlpatterns = patterns('',
    # ex: /games/
    url(r'^$', views.savepicks, name='index'),
    url(r'^yourpicks/$', views.pickwinners, name='makepicks'),
    url(r'^grid/$', views.pickgrid, name='grid'),
    url(r'^leaderboard/$', views.leader, name='leaderboard'),
)

# urlpatterns += staticfiles_urlpatterns()

from django.conf.urls import patterns, include, url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'bowlgames.views.home', name = 'home'),
    url(r'^accounts/', include('accounts.urls', namespace = 'accounts')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^games/', include('picks.urls', namespace = "picks")),
)

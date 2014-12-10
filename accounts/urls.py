from django.conf.urls import patterns, include, url

from accounts import views

urlpatterns = patterns('',
    url(r'^$', views.login_page, name='login_page'),
    url(r'^logoutuser$', views.logout_page, name='logout_page'),
    url(r'^login/', views.login_user, name='login'),
    url(r'^logout/', views.logout_user, name='logout'),
	url(r'^register/', views.register_page, name='registration_page'),
	url(r'^reg/$', views.register_user, name='register'),
)

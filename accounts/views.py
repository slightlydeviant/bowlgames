from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic

# from accounts.models import user models
from django.contrib.auth.models import User

def logout_page(request):
    return HttpResponse("<a href=''>Click to log out</a>")

def login_page(request):
    return render(request, 'accounts/login.html')

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('picks:index'))
        else:
            return render(request, 'accounts/login.html', {
            'error_message': "account is disabled",
        })
    else:
        return render(request, 'accounts/login.html', {
            'error_message': "The username and password were incorrect",
        })

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register_page(request):
    return render(request, 'accounts/register.html')

def register_user(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    pw = request.POST['password']
    pw2 = request.POST['password2']
    current_users_list = User.objects.values_list('username', flat=True)
    if username is not u'' and firstname is not u'' and lastname is not u'' and pw is not u'':
        if username not in current_users_list:
            if pw == pw2:
                user = User.objects.create_user(username = username,
                                                password = pw)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
                user_log = authenticate(username = username, password = pw)
                login(request, user_log)
                return HttpResponseRedirect(reverse('picks:index'))
            else:
                return render(request, 'accounts/register.html', {
                    'error_message': "The passwords did not match. Try again.",
                })
        else:
            return render(request, 'accounts/register.html', {
                    'error_message': "That username is already taken. Please try again.",
                })
    else:
        return render(request, 'accounts/register.html', {
            'error_message': "Field missing. Please try again.",
        })

def register_user2(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    username = request.POST['username']
    pw = request.POST['password']
    pw2 = request.POST['password2']
    if username is not None and firstname is not None and lastname is not None and pw is not None:
        if pw == pw2:
            user = User.objects.create_user(username = username,
                                            password = pw)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            user_log = authenticate(username = username, password = pw)
            login(request, user_log)
            return HttpResponseRedirect(reverse('picks:index'))
        else:
            return render(request, 'accounts/register.html', {
                'error_message': "The passwords did not match. Try again.",
            })
    else:
        return render(request, 'accounts/register.html', {
            'error_message': "Field missing. Please try again.",
        })

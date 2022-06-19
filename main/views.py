from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import secrets
import requests
import json


def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def tic_tac_menu(request):
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        char_choice = request.POST.get('character_choice')
        # print('processing')
        # res = requests.get('http://127.0.0.1:8000/api/v1/game/add-image')
        # json '= res.json()
        # image = 'lol'
        # print(image, ' view')
        if request.user.is_authenticated:
            nickname = request.user.username
        else:
            nickname = request.POST.get('nickname')
               

        return redirect('play/%s?&choice=%s&nickname=%s'%(room_code, char_choice, nickname))
    return render(request, 'main/tic-tac_menu.html', {})


def tic_tac_game(request, room_code):
    choice = request.GET.get('choice')
    nickname = request.GET.get('nickname')
    img = request.GET.get('img')
    if choice not in ['X', 'O']:
        raise Http404('Choice does not exist')
    context = {'char_choice': choice, 'room_code': room_code, 'nickname': nickname, 'img': img}

    return render(request, 'main/tic-tac_game.html', context)


def userRegistration(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')

    context = {'form': form}
    return render(request, 'main/login_register.html', context)


def userLogin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('home')

    context = {'form': form}
    return render(request, 'main/login_register.html', context)


def userLogout(request):
    logout(request)
    return redirect('home')


def topUsersView(request):
    users = User.objects.order_by('-rating')
    context = {'users': users}
    return render(request, 'main/top-list.html', context)


# def chat(request):
    

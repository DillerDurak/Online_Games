from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.views import generic


def index(request):
    context = {}
    return render(request, 'main/index.html', context)

def tic_tac_menu(request):
    if request.method == 'POST':

        room_code = request.POST.get('room_code')
        game,created = Game_tic.objects.get_or_create(name=room_code)

        image = request.POST.get('image')
        choice = request.POST.get('character_choice')

        if request.user.is_authenticated:
            nickname = request.user.username
            rating = request.user.rating
        else:
            nickname = request.POST.get('nickname')
            rating = 0

        print('room_code: ', room_code, 'image: ', image, 'choice: ', choice, 'nickname: ', nickname, 'rating', rating)
        player_to_add = Player_tic(nickname=nickname, choice=choice, image=image, rating=rating)
        player_to_add.save()
        game.player.add(player_to_add)
        response = redirect('play/%s'%(room_code))
        print(f'{player_to_add.nickname} added to {game.name}.')
        response.set_cookie('nickname', nickname)
        response.set_cookie('char_choice', choice)
        response.set_cookie('image', image)

        return response

    return render(request, 'main/tic-tac_menu.html', {})


def tic_tac_game(request, room_code):
    game = Game_tic.objects.get(name=room_code)
    print('name: ', game.name)
    players = game.player.all()
    print(players.values('nickname'))
    try:
        player_1 = players.get(choice='X')
    except:
        player_1 = False
    try:    
        player_2 = players.get(choice='O')
    except:
        player_2 = False
    
    choice = request.COOKIES.get('char_choice')
    nickname = request.COOKIES.get('nickname')
    

    context = {'room_code': room_code, 'player_1': player_1, 'player_2': player_2, 'game': game, 'choice': choice, 'nickname': nickname}

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


def pixelBattle(request):
    context= {}
    return render(request, 'main/canvas.html', context)


def drawBattle(request):
    context = {}
    return render(request, 'main/draw_battle.html', context)
    

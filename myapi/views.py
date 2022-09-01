from django.http import JsonResponse
from django.shortcuts import render
from main.models import *
from .serializers import UserSerializer
from rest_framework.decorators import api_view
import requests
from random import randint
from django.db.models import Q

from main.models import *


@api_view(['POST'])
def add_user(request): 
    data = request.data
    room_code = data['room_code']
    game = Game_tic.objects.get(name=room_code)
    try:
        player1 = Player_tic.objects.filter(player__name=game.name).get(choice='X')
        player2 = Player_tic.objects.filter(player__name=game.name).get(choice='O')
        return JsonResponse({'player_1': player1.image, 'player_2': player2.image})
    except:
        player1 = Player_tic.objects.get(player__name=game.name)
        return JsonResponse({'player_1': player1.image})


@api_view(['POST'])
def add_rating(request):
    data = request.data
    username = data['username']
    user = User.objects.get(username=username)
    user.rating += randint(5,20)
    user.save()

    if user.rating >=30:
        user.rank = Rank.objects.get(title='Bronze')
    if user.rating >=70:
        user.rank = Rank.objects.get(title='Silver')
    if user.rating >=150:
        user.rank = Rank.objects.get(title='Gold')

    user.save()
    return JsonResponse({'message': f'added 20 points to {user.username}'})


@api_view(['POST'])
def delete_user(request):
    data = request.data
    nickname = data.get('nickname')
    player = Player_tic.objects.get(nickname=nickname)
    game = Game_tic.objects.get(player__nickname=player.nickname)
    player.delete()
    print('deleted:', nickname, 'game:', game.name)
    if game.player.count() == 0:
        game.delete()
        print(game.name, ' - deleted')
    
    response = JsonResponse({'Action': 'User deleted'})
    response.delete_cookie('char_choice')
    response.delete_cookie('nickname')
    response.delete_cookie('image')

    return response
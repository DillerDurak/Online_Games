from django.http import JsonResponse
from django.shortcuts import render
from main.models import User, Rank, Player
from .serializers import UserSerializer
from rest_framework.decorators import api_view
import requests
from random import randint

dataList = {'image': '', 'nickname': '', 'count': 0}
count = 0

def fillData(image, nickname, count):
    global dataList
    dataList = {'image': image, 'nickname': nickname, 'count': count}
    print(dataList)


@api_view(['POST', 'GET'])
def add_image(request): 
    global dataList
    global count 
    if request.method == 'POST':
        data = request.data
        image = data.get('image', None)
        nickname = data.get('nickname', None)
        print(image, ' get post from fetch', nickname)
        count += 1 
        fillData(image, nickname, count)   
    else:
        return JsonResponse(dataList)
    return JsonResponse({'OK': '200'})

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
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('tic-tac/', tic_tac_menu, name='tic-tac_menu'),
    path('login/', userLogin, name='login'),
    path('registration/', userRegistration, name='registration'),
    path('logout/', userLogout, name='logout'),
    path('tic-tac/play/<str:room_code>', tic_tac_game, name='tic-tac_game'),
    path('top-list/', topUsersView, name='top-list'),
    path('pixel-battle/', pixelBattle, name='pixel-battle'),
    path('draw-battle/', drawBattle, name='draw-battle'),
]
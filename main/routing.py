from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/tic-tac/play/<room_code>/', consumers.TicTacToeConsumer.as_asgi()),
]
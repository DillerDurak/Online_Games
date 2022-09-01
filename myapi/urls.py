from django.urls import path
from . import views

urlpatterns = [
    path('game/add-user/', views.add_user, name='add-user'),
    path('user/change-rating/', views.add_rating, name='add-rating'),
    path('game/delete-user/', views.delete_user, name='delete-user')
]
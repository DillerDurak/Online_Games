from django.urls import path
from . import views

urlpatterns = [
    path('game/add-image/', views.add_image, name='add-image'),
    path('user/change-rating/', views.add_rating, name='add-rating'),
]
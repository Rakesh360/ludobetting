from django.urls import path,include
from .views import *


urlpatterns = [
    
    path('create_game', create_game , name="create_game"),
    path('waiting_room/<game_slug>' , waiting_room , name="waiting_room"),
    path('payment_success' , payment_success , name="payment_success"),
    path('api/games' , all_games_api , name="all_games_api"),
    path('api/mark_game_waiting/<game_slug>' , mark_game_waiting , name="mark_game_waiting")
    
]
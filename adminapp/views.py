from django.shortcuts import render
from ludoapp.models import *
# Create your views here.


def disputed(request):
    disputed_games = DisputedGame.objects.all()
    context = {'disputed_games': disputed_games}
    return render(request , "admin_panel/disputed.html" , context)

def show_disputed(request , id):
    print(id)
    game = Game.objects.filter(id=id).first()
    print(game)
    game_images = GameImages.objects.filter(game = game)
    context = {'images' : game_images , 'game' : game}
    print(context)
    return render(request , "admin_panel/show_disputed.html" , context)
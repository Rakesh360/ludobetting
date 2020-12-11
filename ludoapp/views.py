from django.shortcuts import render, get_object_or_404, reverse,redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ludoapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ludoapp.forms import add_Coins_form
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage
import random
from .helpers import check_payment_status , make_payment,  random_string_generator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

config = {
        "apiKey": "AIzaSyA5QXTBDrkkt6RKDiEJlz2xVjq_YAL7Jww",
        "authDomain": "ludo-27977.firebaseapp.com",
        "databaseURL":"https://ludo-27977-default-rtdb.firebaseio.com",
        "storageBucket": "ludo-27977.appspot.com",
        "appId" :"1:773216686826:web:2c86813e6a5a284914bd93",
         "measurementId": "G-D84371JPYJ"
        }


def index(request):
    return render(request,"home.html")





def playludo(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        user_info = User_info.objects.filter(user=user ).first()
        request.session['coins'] = user_info.available_coins
        print(request.session['coins'])
        context = {'coins' : user_info.available_coins , 'whatsapp_number' : user_info.whatsapp_number}
    return render(request,"playludo.html" , context)

def playsnackladder(request):
    return render(request,"playsnackladder.html")


@login_required(login_url='/accounts/user_login/')
def buycoins(request):
    context = {}
    if request.method == "POST":
        orderAmount = request.POST.get("orderAmount")
        checkout = {}
        order_id = random_string_generator()
        user_info = User_info.objects.filter(user= request.user ).first()
        result = make_payment(order_id , orderAmount , request.user.username  , str(user_info.whatsapp_number) ,   "s")
        
        checkout = {'signature': result , 'orderAmount' : orderAmount , 'orderId' : order_id ,'customerName' :request.user.username , 'customerPhone' :str(user_info.whatsapp_number) }
        
        context = {'checkout': checkout}
        order_coins = OrderCoins(order_id= order_id , user = request.user , amount=orderAmount)
        order_coins.save()
        return render(request,"buycoins.html" , context)
    return render(request,"buycoins.html" , context)

from datetime import datetime, timedelta

@login_required(login_url='/accounts/user_login/')
def sellcoins(request):
    user = request.user
    if request.method == 'POST':
        number = request.POST.get('number')
        amount = request.POST.get('amount')
        user_info = User_info.objects.filter(user=user , is_paid=False ).first()
        total_request = BetTransaction.objects.filter(user=user,requested_date__gte = datetime.now() - timedelta(days=1))
        if int(amount) > int(user_info.available_coins):
            request.session['message'] = 'You dont have enough coins'
            request.session['class'] = 'danger'
            return redirect('/sellcoins/')
        elif len(total_request) >= 2 :
            request.session['message'] = 'Only 2 request per day are allowed'
            request.session['class'] = 'warning'
            return redirect('/sellcoins/')
        else:
            request.session['message'] = 'Your request has been received'
            request.session['class'] = 'success'
            user_bet = BetTransaction(user = user , coins= amount)
            user_bet.save()
            return redirect('/sellcoins/')
            
        
    user_info = User_info.objects.filter(user=user ).first()
    
    
    sell_coins = BetTransaction.objects.filter(user=user)
    context = {'coins' : user_info.available_coins , 'whatsapp_number' : user_info.whatsapp_number, 'sell_coins' :sell_coins}
    return render(request,"sellcoins.html", context)

def terms(request):
    return render(request,"term_condition.html")

def contactpage(request):
    
    if request.method=="POST":
        nm = request.POST["name"]
        con = request.POST["contact"]
        sub = request.POST["subject"]
        msz = request.POST["message"]

        data = Contact_Us(name=nm,contact_number=con,subject=sub,message=msz)
        data.save()
        res = "Dear {} Thanks for your massage we will contact you soon".format(nm)
        return render(request,"contact.html",{"status":res})
    return render(request,"help.html")


@login_required(login_url='/accounts/user_login/')
def history(request):
    user = request.user
    order_coins = OrderCoins.objects.filter(user=user)
    penaltys = Penalty.objects.filter(user=user)
    payouts = BetTransaction.objects.filter(user=user)
    game_win_loose = GameWinnerLoose.objects.filter(user=user)
    
    results = []
    for order_coin in order_coins:
        result = {}
        result['amount'] = order_coin.amount
        result['date'] = order_coin.added_on
        result['transaction'] = order_coin.status
        if order_coin.status is True:
            result['remark'] = 'Your ordered coins succesfull'
        else:
            result['remark'] = 'Your transaction was failed'
        results.append(result)
        
    for penalty in penaltys:
        result = {}
        result['amount'] = penalty.amount
        result['date'] = penalty.added_on
        result['transaction'] = True
        result['remark'] = 'You got penalty'
        result['reason'] = penalty.reason_of_penalty
        results.append(result)
    
    for payout in payouts:
        result = {}
        result['amount'] = payout.coins
        result['transaction'] = payout.is_paid
        result['date'] = payout.requested_date
        result['remark'] = 'Sold by You'
        results.append(result)
        
        
    for game in game_win_loose:
        result = {}
        result['amount'] = game.amount
        result['transaction'] = game.win_or_lost
        result['date'] = game.date
        if game.win_or_lost:
            result['reason'] = 'Win from' + game.game.user_one +' vs '+ game.game.user_two
        else:
            result['reason'] = 'Loose from ' + game.game.user_one +' vs ' + game.game.user_two
        result['remark'] = 'Coins for game winning or loosing'
        results.append(result)
        

    final_results = sorted(results , key=lambda i:i ['date'])
    (final_results).reverse()
    context = {'results': final_results}
    return render(request,"history.html",context)


@csrf_exempt
def payment_success(request):
    data  = (request.body)
    
    
    decode_data = data.decode("utf-8") 
    raw_data = decode_data.split("&")
    order_id = raw_data[0].split("=")
    order_amount = raw_data[1].split('=')
    transaction_status = raw_data[3].split("=")
    
    order_coins = OrderCoins.objects.filter(order_id=order_id[1]).first()
    if transaction_status[1] == 'SUCCESS':
        user_info = User_info.objects.filter(user=order_coins.user).first()
        user_info.available_coins += int(float((order_amount[1])))
        user_info.save()
        order_coins.status = True
        order_coins.save()
        return render(request,"success.html")
    return render(request,"error.html")
        


import json
from django.http import JsonResponse
import uuid
from firebase import firebase
import pyrebase

   
@csrf_exempt
def create_game(request):
    data = json.loads(request.body)
    user = request.user
    user_info = User_info.objects.filter(user = user).first()
    
    if data.get('coins') is None:
        return JsonResponse({'message': 'coins is required'})
    
    if user_info.available_coins < int(data.get('coins')):
        return JsonResponse({'message' : 'You dont have enough coins.' , 'status' : False}) 
    
    game_slug = uuid.uuid4()
    game_start = GameStart.objects.get_or_create(game_created_by = user  ,game_status='PENDING')
    game_start.game_slug
    game_start.game_amount=data.get('coins') 
    
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    data = {"game_slug": (str(game_slug) ) ,
            "game_amount" :  data.get('coins'),
            'game_created_by' : request.user.username,
            "room_code" : '',
            'game_status' : 'PENDING',
            'user_one' : user.id,
            'user_two' : ''
            }
    result = db.child("game").push(data)
    game_start.firebase_id = result['name']
    game_start.save()

    return JsonResponse({'message' : 'Game started','game_start' :game_start.id ,'room_id' : (str(game_slug) ) , 'status' :True})

from rest_framework.decorators import api_view
@api_view()
def all_games_api(request):
    user_id = request.query_params.get('user_id')

    if user_id is not None:
        user = User.objects.get(id=user_id)
        game_by_user = GameStart.objects.filter(game_status = 'PENDING' ,game_created_by = user).first()
        games_start = GameStart.objects.filter(game_status = 'PENDING').exclude(game_created_by=request.user)
    
    else:
        user = User.objects.first()
        game_by_user =[]
        games_start = GameStart.objects.filter(game_status = 'PENDING')
    
        
    #game_by_user = GameStart.objects.filter(game_status = 'PENDING' ,game_created_by = user).first()
    #games_start = GameStart.objects.filter(game_status = 'PENDING').exclude(game_created_by=request.user)
    games = []
    
    raw_running_games = Game.objects.all()[0:10]
    running_games = []
    for raw in raw_running_games:
        game = {}
        game['game_amount'] = raw.betting_amount
        game['between'] = raw.user_one.username + ' vs ' + raw.user_two.username
        running_games.append(game)    
    
    
    
    for gs in games_start:
        game = {}
        game['game_created_by'] = gs.game_created_by.username + 'set a challenge for '
        game['game_slug'] = gs.game_slug
        game['game_status'] = gs.game_status
        game['game_amount'] = gs.game_amount
        game['firebase_id'] = gs.firebase_id
        games.append(game)
    
    user_created_game = {}
    if game_by_user:
        user_created_game['game_created'] = game_by_user.game_created_by.username
        user_created_game['game_amount'] = game_by_user.game_amount
        user_created_game['game_slug'] = game_by_user.game_slug
        user_created_game['game_id'] = game_by_user.id
        
        
    
    result = {}
    result['game_by_user'] = user_created_game
    result['all_games'] = games
    result['running_games'] = running_games
    
    
    return JsonResponse(result , safe  =False)
        
@login_required(login_url='/accounts/user_login/')
def mark_game_waiting(request , game_slug):
    user = request.user
    game_start = GameStart.objects.filter(game_slug=game_slug).first()
    game_start.game_status = 'WAITING'
    game_start.save()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    result = db.child("game").child(game_start.firebase_id).update({'user_two' : user.id})
    game = Game(game_start = game_start , betting_amount=game_start.game_amount)
    game.save()
    return JsonResponse({'status': True , 'message': 'Game in waiting'})
@login_required(login_url='/accounts/user_login/')
def waiting_room(request , game_slug):
    game_start = GameStart.objects.filter(game_slug= game_slug).first()
    context = {'firebase_id' : game_start.firebase_id , 'game_slug' :game_start.game_slug , 'game_amount' : game_start.game_amount , 'created_by' : game_start.game_created_by.id} 
    if request.method == 'POST':
        game_result = request.POST.get('game_result')
        images = request.FILES.getlist('upload_file')
        game_start = GameStart.objects.filter(game_slug=request.POST.get('game_slug')).first()
        user_one = User.objects.get(id = request.POST.get('user_one') )
        user_two = User.objects.get(id = request.POST.get('user_two') )
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        result = db.child("game").child(game_start.firebase_id).get()
        game_start.game_status = 'OVER'
        game_start.save()
        
        
        room_code = None
        for key in result.each():
            if key.key() == 'room_code':
                room_code = (key.val())
                
        game = Game.objects.filter(game_start = game_start).first()
        game.user_one = user_one
        game.user_two = user_two
        game.room_code = room_code
        
        if game.result_user_one is None and request.user == user_one:
            game.result_user_one = game_result
        
        if game.result_user_two is None and request.user == user_two:
            game.result_user_two = game_result

        game.save()
        for image in images:
            game_image_obj = GameImages(game=game , images=image)
            game_image_obj.save()
        return redirect('/success/')
    return render(request, 'waiting.html' , context)


@login_required(login_url='/accounts/user_login/')
def delete_game(request , id):
    try:
        game = GameStart.objects.get(id=id)
        game.delete()
    except GameStart.DoesNotExist:
        return redirect('/')
    return redirect('/')
    
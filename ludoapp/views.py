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
    user = request.user
    user_info = User_info.objects.filter(user=user ).first()
    print(user_info.whatsapp_number)
    context = {'coins' : user_info.available_coins , 'whatsapp_number' : user_info.whatsapp_number}
    return render(request,"playludo.html" , context)

def playsnackladder(request):
    return render(request,"playsnackladder.html")

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



def sellcoins(request):
    user = request.user
    if request.method == 'POST':
        number = request.POST.get('number')
        amount = request.POST.get('amount')
        user_info = User_info.objects.filter(user=user ).first()
        
        if int(amount) > int(user_info.available_coins):
            request.session['message'] = 'You dont have enough coins'
            request.session['class'] = 'danger'
            return redirect('/sellcoins/')
        else:
            request.session['message'] = 'Your request has been received'
            request.session['class'] = 'success'
            user_bet = BetTransaction(user = user , coins= amount)
            user_bet.save()
            return redirect('/sellcoins/')
            
        
    user_info = User_info.objects.filter(user=user ).first()
    
    
    print(user_info.whatsapp_number)
    context = {'coins' : user_info.available_coins , 'whatsapp_number' : user_info.whatsapp_number}
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



def history(request):
    user = request.user
    order_coins = OrderCoins.objects.filter(user=user)
    penaltys = Penalty.objects.filter(user=user)
    payouts = BetTransaction.objects.filter(user=user)
    
    
    context = {'order_coins': order_coins, 'penaltys': penaltys , 'payouts' : payouts}
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
    game_start = GameStart(game_created_by = user , game_slug=game_slug , game_status='PENDING' , game_amount=data.get('coins') )
    
    
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
    games_start = GameStart.objects.filter(game_status = 'PENDING').exclude(game_created_by=request.user)
    games = []
    for gs in games_start:
        game = {}
        game['game_created_by'] = gs.game_created_by.username
        game['game_slug'] = gs.game_slug
        game['game_status'] = gs.game_status
        game['game_amount'] = gs.game_amount
        game['firebase_id'] = gs.firebase_id
        games.append(game)
    return JsonResponse(games , safe  =False)
        
        
def mark_game_waiting(request , game_slug):
    user = request.user
    game_start = GameStart.objects.filter(game_slug=game_slug).first()
    game_start.game_status = 'WAITING'
    game_start.save()
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    result = db.child("game").child(game_start.firebase_id).update({'user_two' : user.id})
    return JsonResponse({'status': True , 'message': 'Game in waiting'})

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
        game = Game(
                    game_start = game_start , user_one = user_one,
                    user_two = user_two, betting_amount=game_start.game_amount,
                    room_code = result['room_code']
                    )
        game.save()
        for image in images:
            game_image_obj = GameImage(game=game , images=image)
            image.save()
        
    return render(request, 'waiting.html' , context)
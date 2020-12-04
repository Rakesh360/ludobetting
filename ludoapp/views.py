from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ludoapp.models import Contact_Us,  User_info, Add_coins,Sell_coins
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from ludoapp.forms import add_Coins_form
from django.db.models import Q
from datetime import datetime
from django.core.mail import EmailMessage
import random
from .helpers import check_payment_status




def index(request):
    return render(request,"home.html")

def playludo(request):
    return render(request,"playludo.html")

def playsnackladder(request):
    return render(request,"playsnackladder.html")

def buycoins(request):
    context = {}
    if request.method == "POST":
        order_id = request.POST.get("txnId")
        amount = request.POST.get("amount")
        response = check_payment_status(order_id , amount)
        payment_status = str(response['body']['resultInfo']['resultCode'])
      
        if payment_status == '01':
            pass
        elif payment_status == '334':
            message = 'Invalid transaction id'
        elif payment_status == '335':
            message = 'Your transaction was failed'
        elif payment_status == '400':
            message = 'Your transaction is pending try after some time'
        else:
            message = 'Your transaction was failed'
        
        context = {'message': message}
    print(context)
    return render(request,"buycoins.html" , context)

def sellcoins(request):
    return render(request,"sellcoins.html",)

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
    return render(request,"history.html",context)




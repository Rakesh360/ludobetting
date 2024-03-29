from django.shortcuts import render, get_object_or_404, reverse,redirect,HttpResponseRedirect
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
import cryptocode
from cryptography.fernet import Fernet
from .helpers import send_otp
from django.http import JsonResponse


from django.views.decorators.csrf import csrf_exempt

def register(request):
    if "user_id"in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User,id=uid)
        login(request,usr)
        if usr.is_superuser:
            return HttpResponseRedirect("/admin")
        if usr.is_active:
            return HttpResponseRedirect("/index")
    if request.method=="POST":
        fname = request.POST["first"]
        lname = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        con = request.POST["contact"]
        term = request.POST["agreement"]
        
        
        user_by_username = User.objects.filter(username= un).first()
        user_by_mobile = User_info.objects.filter(whatsapp_number=con).first()
        print(user_by_username)
        if user_by_username:
            return render(request,"home.html",{"status":"This user name is already taken".format(un)})
        
        if user_by_mobile:
            return render(request,"home.html",{"status":"This mobile number is already taken".format(con)})  
            
        
        
        usr = User(username = un , email = em , first_name=fname, last_name=lname  )
        usr.set_password(pwd)
        usr.save()

        otp = send_otp(con)
        reg = User_info(user=usr, whatsapp_number=con , otp = otp)
        reg.save()
        encrypted_user_id = str(usr.id)
        return HttpResponseRedirect('/accounts/verify_otp/'+ (encrypted_user_id))
    return render(request,"register.html")


def verify_otp(request, id):
    if request.method == "POST":
        otp = request.POST.get('otp')
        user = User_info.objects.filter(user = id).first()
        if str(otp) == str(user.otp):
            user.is_verified = True
            user.save()
            return redirect(user_login)
        else:
            context = {'message': 'Wrong OTP'}
            return render(request,'otp.html', context)
    
    context = {'user_id' : id}
    return render(request,"otp.html", context)

@csrf_exempt
def resend_otp(request , id):
    user = User_info.objects.filter(user = id).first()
    otp  = send_otp(user.whatsapp_number)
    user.otp =otp
    user.save()
    return JsonResponse({"status":"Otp Sent"})
     



def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def user_login(request):
    if request.method=="POST":
        whatsapp_number = request.POST["whatsapp"]
        pwd = request.POST["password"]

        user_whatsapp = User_info.objects.filter(whatsapp_number = whatsapp_number).first()
        
        if user_whatsapp is None:
            return render(request,"login.html",{"error":"User not found"})

        user = authenticate(username=user_whatsapp.user.username,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                res = HttpResponseRedirect("/")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now())
                return res
        else:
            return render(request,"login.html",{"error":"Invalid Username or Password"})
    else:
        return render(request,"login.html")    
    
    
def user_logout(request):
    logout(request)
    res =  HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    return res

def edit_profile(request):       
    return render(request,"edit_profile.html")

def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)

def forget_password(request):
    context = {}
    if request.method=="POST":
        un = request.POST["mobile"]
        user_by_username = User_info.objects.filter(whatsapp_number= un).first()
       
        if user_by_username is None:
            return render(request,"forgot_pass.html",{"status":"User not found".format(un)})
        
        otp = send_otp(user_by_username.whatsapp_number)
        user_by_username.otp = otp
        user_by_username.save()
        encrypted_user_id = str(user_by_username.user.id)
        return HttpResponseRedirect('/accounts/verify_otp_forget_password/'+ (encrypted_user_id))
    return render(request,"forgot_pass.html",context)



def verify_otp_forget_password(request, id):
    if request.method == "POST":
        otp = request.POST.get('otp')
        
        user = User.objects.filter(id=id).first()
        print(user)
        user_info = User_info.objects.filter(user = user).first()
        print(user_info)
        if str(otp) == str(user_info.otp):
            authenticated_user = User.objects.get(id=id)
            login(request , authenticated_user)
            return redirect('/accounts/change_password_final/')
            return redirect(user_login)
        else:
            context = {'message': 'Wrong OTP'}
            return render(request,'otp.html', context)
    
    context = {'user_id' : id}
    return render(request , "verify_otp_forget_password.html" , context)


def change_password_final(request):
    if request.method == "POST":
        new_pas = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_pas != confirm_password:
            context = {'message': 'Both password and confirm password  should be same'}
            return render(request , "change_password_final.html" , context)
            
        
        user = User.objects.get(id = request.user.id)
        user.set_password(new_pas)
        user.save()
        context = {'message': 'Password changed'}
        return render(request , "change_password_final.html" , context)
        
    return render(request , "change_password_final.html")
    



def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \nMyWebsite".format(user.username, otp)
        try:
            email = EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})
    except:
        return JsonResponse({"status":"failed"})
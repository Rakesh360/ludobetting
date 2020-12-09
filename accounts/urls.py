from django.urls import path,include
from accounts import views



urlpatterns = [
    
    path("signup/",views.register,name="reg"),
    path("check_user/",views.check_user,name="check_user"),
    path("user_login",views.user_login,name="user_login"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("change_password/",views.change_password,name="change_password"), 
    path("forget_password",views.forget_password, name="forget_password"),
    path("reset_password",views.reset_password,name="reset_password"),
    path("verify_otp/<int:id>" , views.verify_otp , name="verify_otp"),
    path("resend_otp/<id>" , views.resend_otp , name="resend_otp"),
    
    path("user_logout" , views.user_logout , name="user_logout"),
    
    
    path("verify_otp_forget_password/<id>" , views.verify_otp_forget_password  , name="verify_otp_forget_password"),
    
    
    path("change_password_final/" , views.change_password_final , name="change_password_final")   
]
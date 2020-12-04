from django.urls import path,include
from accounts import views



urlpatterns = [
    
    path("signup/",views.register,name="reg"),
    path("check_user/",views.check_user,name="check_user"),
    path("user_login",views.user_login,name="user_login"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path("change_password/",views.change_password,name="change_password"), 
    path("forgotpass",views.forgotpass, name="forgotpass"),
    path("reset_password",views.reset_password,name="reset_password"),
    path("verify_otp/<int:id>" , views.verify_otp , name="verify_otp"),
    path("resend_otp/<id>" , views.resend_otp , name="resend_otp")
    
]
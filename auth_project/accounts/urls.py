from django.urls import path
from .views import signup,user_login,user_logout,home,reset_pass,forget_password,reset_password,verify_otp

urlpatterns = [

    path('',home,name = "home"),
    path('signup/',signup,name ="signup"),
    path('login/',user_login, name = "login"),
    path('logout/',user_logout,name = "logout"),
    path('resetpass/',reset_pass,name= "resetpass"),
    path('forgetpass/',forget_password,name = "forgetpassword"),
    path("reset-password/<str:token>/", reset_password, name="reset_password"),
    # path("otp/", otp, name="otp"),  # Send OTP after entering email
    path("verify-otp/", verify_otp, name="verify_otp"),
    
]
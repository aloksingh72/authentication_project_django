from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.utils.crypto import get_random_string
# Create your views here.


#  for  signup view
def signup(request):
    if request.method == "POST":
        username  = request.POST["username"]
        email  = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        print(username,email,password,confirm_password)
        
        if UserDetails.objects.filter(email = email).exists():
            messages.error(request,"Email is already exists")
            return redirect("signup")
        # checking if passwords match
        if password != confirm_password :
            messages.error(request,"Passwords do not match")
            return redirect("signup")

       

         #checking wheather user is exists or not
        if UserDetails.objects.filter(username = username).exists():
            messages.error(request,"username is already exists")
            return redirect("signup")
        # if not then create the new user using create_user method 
        user  = UserDetails()
        user.username = username
        user.email = email
        user.password = password
        user.confirm_password = confirm_password
        user.save()
        messages.success(request, "Accounts created successfully")
        return redirect("login")
    return render(request,"signup.html")

# login view
def user_login(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user_instance=UserDetails.objects.filter(username= username , password=password).last()
        # user = authenticate(request,username = username, password = password)
        if user_instance is not None:
            # store the session data for authentication 
            messages.success(request,f"Welcome{username}!")
            return redirect("home")
        else:
            messages.error(request,"Invalid username and password")
            return redirect("login")
    return render(request,"login.html")


#logout view
def user_logout(request):
    logout(request)  # clears the session data logged the user out
    messages.success(request,"You have been logged out")
    return redirect("login")


# Home view for logged in user
def home(request):
    return render(request,"home.html")

# view for resetting the password
def reset_pass(request):
    if request.method =="POST":
        username = request.POST.get("username")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")
    

         # checking if user exists or not
        user_instance = UserDetails.objects.filter(username = username,password = old_password).last()
        print(user_instance)
        if not user_instance:
            messages.error(request,"old password is incorrect")
            return redirect("resetpass")

        if new_password != confirm_password:
            messages.error(request,"password not matched")
            return redirect("resetpass")
        
        # update in the database
        user_instance.password = new_password
        user_instance.confirm_password = confirm_password
        user_instance.save()

        messages.success(request,"password changed successfully")
        return redirect("login")


    return render(request,"resetpass.html")


# stores tokens temporarialy
reset_tokens={}
def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # checking if email exists
        user_instance = UserDetails.object.filter(email =email).first()
        if not user_instance:
            message.error(request,"Email not found...")
            return redirect("forget_password")
        # generate reset tokens
        reset_token =   get_random_string(32)
        reset_tokens[email]= reset_token

        # send the reset email
        rest_link = f"http://127.0.0.1:8000/reset-password/{reset_token}/"
        send_mail(
            "Password Reset Request",
            f"Click the link to reset your password: {reset_link}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        messages.success(request,"Password send to your email")
        return redirect("login")
    return render(request,"forgetpassword.html")



    return render(request,"forgetpassword.html")






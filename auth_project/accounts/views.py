from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


#  for  signup view
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username = username).exists():
            messages.error(request,"username is already exists")
            return redirect("signup")
        
        user  = User.objects.create_user(username = username,email = email,password = password)
        user.save()
        messages.success(request, "Accounts created successfully")
        return redirect("login")
    return render(request,"signup.html")

# login view
def user_login(request):
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request,username = username, password = password)
        if user is not None:
            login(request,user) # store the session data for authentication 
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

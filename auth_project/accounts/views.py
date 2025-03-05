from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from datetime import datetime
import random
# Create your views here.


#  for  signup view
def signup(request):
    if request.method == "POST":
        print(datetime.now())
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

# login view with uername

# def user_login(request):
#     if request.method =="POST":
#         username = request.POST["username"]
#         password = request.POST["password"]

#         user_instance=UserDetails.objects.filter(username= username , password=password).last()
#         # user = authenticate(request,username = username, password = password)
#         if user_instance is not None:
#             # store the session data for authentication 
#             messages.success(request,f"Welcome{username}!")
#             return redirect("home")
#         else:
#             messages.error(request,"Invalid username and password")
#             return redirect("login")
#     return render(request,"login.html")


# login the user using the email id and password
def user_login(request):
    if request.method =="POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user_instance = UserDetails.objects.filter(email = email,password = password).last()

        if user_instance is not None:
            print(user_instance.username)
            otp_code = str(random.randint(1000, 9999))

            # Store OTP in the database
            user_instance.otp_code = otp_code
            user_instance.save()

            # Send OTP via email
            subject = "Your OTP for Login"
            message = f"Your OTP for login is: {otp_code}. Please enter this OTP to proceed."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            try:
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, "OTP has been sent to your email.")
                # return redirect(f"/verify-otp/?email={email}")  # Redirect to OTP page with email
                return render(request, 'otp.html',context={'email':email})
            except Exception as e:
                messages.error(request, "Failed to send OTP. Please try again.")
                print("Email sending error:", e)
                return redirect("login")

        else:
            messages.error(request,"Invalid email or password")
            return redirect("login")

    return render(request,"login.html")


# # Step 2: Verify OTP
def verify_otp(request):
    if request.method == "POST":
        
        email = request.POST.get("email")  # Retrieve email from URL
        entered_otp = request.POST.get("otp")  # Get OTP entered by user
        print(email)
        user_instance = UserDetails.objects.filter(email=email).last()
        print(user_instance,'----------') 
        if user_instance and user_instance.otp_code == entered_otp:
            # Clear OTP after successful verification
            # user_instance.otp_code = None
            # user_instance.save()
            

            messages.success(request, "OTP verified successfully! Redirecting to home...")
            return render(request,"home.html")  # Redirect to home page
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")

    return render(request, "otp.html")

#logout view
def user_logout(request):
    logout(request)  # clears the session data logged the user out
    messages.success(request,"You have been logged out")
    return redirect("login")


# Home view for logged in user
def home(request):
    # user_instance = UserDetails.objects.get(id=user_id)
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
        user_instance = UserDetails.objects.filter(email = email).first()
        if not user_instance:
            messages.error(request,"Email not found...")
            return redirect("forgetpassword")
        # generate reset tokens
        reset_token =   get_random_string(32)
        reset_tokens[email]= reset_token
        print(email,'<-------------email------------>')
        # send the reset email
        reset_link = f"http://127.0.0.1:8000/reset-password/{reset_token}/"
        subject="Password Reset Request"
        message=f"Click the link to reset your password: {reset_link}"
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
        )
        
        messages.success(request,"Password send to your email")
        return redirect("login")
    return render(request,"forgetpassword.html")



    return render(request,"forgetpassword.html")




def reset_password(request, token):
    # Find email from stored tokens
    email = None
    for key, value in reset_tokens.items():
        if value == token:
            email = key
            break

    if not email:
        messages.error(request, "Invalid or expired reset link.")
        return redirect("login")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect(f"/reset-password/{token}/")

        # Update password in database
        user_instance = UserDetails.objects.get(email=email)
        user_instance.password = new_password
        user_instance.confirm_password = confirm_password
        user_instance.save()

        # Remove token after successful reset
        del reset_tokens[email]

        messages.success(request, "Password reset successful. Please log in.")
        return redirect("login")

    return render(request, "new_password.html")




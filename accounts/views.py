import email
import re
from tkinter.messagebox import NO
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def home(request):
    return render(request, 'home.html')


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        print(user_obj)
        if user_obj is None:
            messages.success(request, 'User Not found')
            return redirect('/login')
        
        profile_obj = Profile.objects.filter(user= user_obj).first()

        if not profile_obj.is_varified:
            messages.success(request, 'User is not varified, Please check your mail')
            return redirect('/login')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong Password')
            return redirect('/login')
        
        login(request, user)
        return redirect('home')


    return render(request, 'login.html')

def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken')
                return redirect('/register')
            
            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken')
                return redirect('/register')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token )
            return redirect('/token')
        except Exception as e:
            print(e)



    return render(request, 'register.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

def varify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_varified:
                messages.success(request, 'Your account is already varified')
                return redirect('/login')
            profile_obj.is_varified = True
            profile_obj.save()
            messages.success(request, 'Your account has been varified')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)

def error_page(request):
    return render(request, 'error.html')



def send_mail_after_registration(email, token):
    subject = "Your account needs to be varified"
    message = f'Hi past the link to varify your account http://127.0.0.1:8000/varify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def logout_attempt(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('/login')
    
    

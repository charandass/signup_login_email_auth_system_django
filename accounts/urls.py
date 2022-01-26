from django import views
from django.contrib import admin
from django.urls import path
from . views import * 


urlpatterns = [
    path('', home, name='home'),
    path('register', register_attempt, name='register_attempt'),
    path('login', login_attempt, name='login_attempt'),
    path('token', token_send, name='token_send'),
    path('success', success, name='success'),
    path('varify/<auth_token>', varify, name='varify'),
    path('error', error_page, name='error_page'),
    path('logout', logout_attempt, name='logout_attempt')

]
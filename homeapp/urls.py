from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_signup, name='login_signup'),
    path('signup', views.handleSignup, name='handleSignup'),
    path('login', views.handleLogin, name='handleLogin'),
    path('delete', views.handleDelete, name='handleDelete'),
    path('home', views.home, name='home'),
    path('logout', views.handleLogout, name='handleLogout')
]

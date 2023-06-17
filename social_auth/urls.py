from django.urls import path,include
from django.conf import settings
from django.contrib import admin
from . import views

urlpatterns = [
    path('create-google-user/', views.google_auth),
    path('create-facebook-user/', views.facebook_auth),
]


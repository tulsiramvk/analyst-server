from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from . import views

urlpatterns = [
    # -----------------------------------------------------------
    path('view-research-product/', views.view_research_product),
    path('create-research-product/', views.create_research_product),
    path('update-research-product/<int:id>/', views.update_research_product),
    path('delete-research-product/<int:id>/', views.delete_research_product),
    # -----------------------------------------------------------
    path('view-research-updates/', views.view_research_updates),
    path('create-research-updates/', views.create_research_updates),
    path('update-research-updates/<int:id>/', views.update_research_updates),
    path('delete-research-updates/<int:id>/', views.delete_research_updates),
    # -----------------------------------------------------------
    path('create-lotsize/', views.create_lotsize),
    path('view-lotsize/', views.view_lotsize),
    path('update-lotsize/<int:id>/', views.update_lotsize),
    path('delete-lotsize/<int:id>/', views.delete_lotsize),
    # -----------------------------------------------------------
    path('create-expiry/', views.create_expiry),
    path('view-expiry/', views.view_expiry),
    path('update-expiry/<int:id>/', views.update_expiry),
    # --------------------------------------------------------
    path('send-call/', views.send_call),
    path('send-update/', views.send_update),
    path('fetch-call/', views.fetch_call),
    # ---------------------------App Inbox Urls---------------------------
    path('fetch-inbox/', views.fetch_inbox),
    path('fetch-my-call/', views.fetch_my_call),    
    path('fetch-today-calls/', views.fetch_today_calls),    
]

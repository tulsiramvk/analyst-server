from django.urls import path,include
from django.conf import settings
from django.contrib import admin
from . import views

urlpatterns = [
    path('create-package/', views.create_package),
    path('view-package/', views.view_package),

    # ----------------Category Urls---------------------
    path('view-category/', views.view_category),
    path('create-category/', views.create_category),
    path('update-category/<int:id>/', views.update_category),
    path('delete-category/<int:id>/', views.delete_category),

    # ----------------Product Urls---------------------
    path('view-product/', views.view_product),
    path('create-product/', views.create_product),
    path('update-product/<int:id>/', views.update_product),
    path('delete-product/<int:id>/', views.delete_product),

    # ----------------Packages Urls---------------------
    path('view-packages/', views.view_packages),
    path('create-packages/', views.create_packages),
    path('update-packages/<int:id>/', views.update_packages),
    path('delete-packages/<int:id>/', views.delete_packages),
    # -----------------Service Urls-----------------------
    path('create-transactions/', views.create_transactions),
    path('view-transactions/', views.view_transactions),
    # -------------Subscription Urls-------------------------
    path('view-active-subscription/', views.view_active_supscription),
    path('view-upcoming-subscription/', views.view_upcoming_subscription),

    # ----------------Banner Urls---------------------
    path('view-banner/', views.view_banner),
    path('create-banner/', views.create_banner),
    path('update-banner/<int:id>/', views.update_banner),
    path('delete-banner/<int:id>/', views.delete_banner),
    
    # ----------------Banner Urls---------------------
    path('view-sar/', views.view_sar),
    path('create-sar/', views.create_sar),
    path('update-sar/<int:id>/', views.update_sar),
    path('delete-sar/<int:id>/', views.delete_sar),

    # -------------Cron Job Urls-------------------------
    path('service-update-job/', views.service_update_job),



    
]

from django.urls import path,include
from django.conf import settings
from django.contrib import admin
from . import views

urlpatterns = [
    path('social-auth/', include('social_auth.urls')),
    path('create-user/', views.create_user),
    path('email-check/', views.email_check),
    path('phone-check/', views.phone_check),
    path('email-login/', views.email_login),
    path('crm-login/', views.crm_login),
    path('forgot-password/', views.forgot_password),
    path('change-password/', views.change_password),
    path('password-change/', views.password_change),
    # -----------------User Profile Relation Url--------------
    path('view-users/', views.view_users),
    path('view-user/<int:id>/', views.view_user),
    path('fetch-user/', views.fetch_user),
    path('change-dp/', views.change_dp),
    path('change-name/', views.change_name),
    # ---------------OTP Generate Urls-------------------------
    path('email-otp-generate/<str:email>/', views.email_otp_generation),
    path('phone-otp-generate/<str:phone>/', views.phone_otp_generation),
    path('register-otp-verify/<str:phone>/<str:email>/', views.register_otp_verify),
]

from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import re
from typing import Dict, Any
from . models import User, EmailVerifications, PhoneVerifications
from . import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
import threading
import datetime
import base64
import pyotp
import requests

# Create your views here.
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.datetime.now()) + "Some Random Secret Key"

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def serialize_user(user: User,token:Token) -> Dict[str, Any]:
    return {
        'id': user.id,
        'last_login': user.last_login.isoformat() if user.last_login is not None else None,
        'is_superuser': user.is_superuser,
        'name': user.name,
        'phone': user.phone,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'email_verify': user.email_verify,
        'proimg': user.proimg if user.proimg else None,
        'created_at': user.created_at.isoformat(),
        'auth_provider':user.auth_provider,
        'user_type':user.user_type,
        'token': token.key
    }

@api_view([
    'POST',
])
def create_user(request):
    if request.method== 'POST':
        u=User.objects.filter(email=request.data['email'])
        if not re.search(r"^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$", request.data['email']):
            return Response("Email Address Not Valid.",status=400)
        elif len(u)>0:
            return Response("Email Already Registered. Continue to login with "+u[0].auth_provider,status=400)
        elif len(request.data['password'])<6:
            return Response("Please Enter Password.",status=400)
        elif len(request.data['phone']) != 10:
            return Response("Please Enter Valid Phone Number.",status=400)
        elif len(User.objects.filter(phone=request.data['phone']))>0:
            return Response("Phone Already Registered.",status=400)
        user = User(name=request.data['name'],user_type='CLIENT',email=request.data['email'],phone=request.data['phone'],proimg=None)
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        serializer = serialize_user(user,token)
        return Response(serializer,status=200)

@api_view([
    'POST',
])
def change_password(request):
    if request.method== 'POST':
        e = EmailVerifications.objects.filter(email=request.data['email'],otp=request.data['otp'])
        if e.exists():
            e.delete()
            user = User.objects.get(email=request.data['email'])
            user.set_password(request.data['password'])
            user.save()
            return Response('OK',status=200)
        else:
            return Response('Wrong OTP',status=400)

@api_view([
    'POST',
])
def password_change(request):
    if request.method== 'POST':
        e = User.objects.get(email=request.data['email'])
        user = authenticate(email=request.data['email'], password=request.data['oldPassword'])
        if user:
            user.set_password(request.data['newPassword'])
            user.save()
            return Response('OK',status=200)
        else:
            return Response('Authentication Failed.',status=400)


@api_view([
    'POST',
])
def forgot_password(request):
    if request.method== 'POST':
        user = User.objects.filter(email=request.data['email'])
        email = request.data['email']
        if user.exists():
            if user[0].auth_provider=='email':
                keygen = generateKey()
                key = base64.b32encode(keygen.returnValue(email).encode())  # Key is generated
                OTPEMAIL = pyotp.HOTP(key)
                b = EmailVerifications.objects.filter(email = email).delete()
                e = EmailVerifications.objects.create(email=email,otp=OTPEMAIL.at(1))
                sub = "Email OTP "
                msg = OTPEMAIL.at(1)+" is your OTP to change Password."
                f = "24x7analyst@gmail.com"
                to = email
                email = EmailMessage(sub,msg,f,[to])
                email.content_subtype = "html"
                EmailThread(email).start()
                return Response('OK',status=200)
            else:
                return Response('Please Continue Login with '+user[0].auth_provider,status=400)
        else:
            return Response('Email Not Registered Please Create Account.',status=400)

@api_view([
    'POST',
])
def email_login(request):
    if request.method== 'POST':
        u=User.objects.filter(email=request.data['email'])
        if u.exists():
            if u[0].auth_provider != 'email':
                return Response('Please continue your login using ' + u[0].auth_provider,status=400)
            else:
                user = authenticate(email=request.data['email'], password=request.data['password'])
                if user is not None and not user.is_staff:
                    Token.objects.filter(user=user).delete()
                    token = Token.objects.create(user=user)
                    user.last_login=timezone.now()
                    user.save()
                    serializer = serialize_user(user,token)
                    return Response(serializer,status=200)
                else:
                    return Response('Invalid Credentials',status=400)
        else:
            return Response("Email Does'nt Exist! Please Register.",status=400)
@api_view([
    'POST',
])
def crm_login(request):
    if request.method== 'POST':
        u=User.objects.filter(email=request.data['email'])
        if u.exists():
            user = authenticate(email=request.data['email'], password=request.data['password'])
            if user is not None and user.is_staff:
                Token.objects.filter(user=user).delete()
                token = Token.objects.create(user=user)
                user.last_login=timezone.now()
                user.save()
                serializer = serialize_user(user,token)
                return Response(serializer,status=200)
            else:
                return Response('Invalid Credentials',status=400)
        else:
            return Response("Email Does'nt Exist! Please Register.",status=400)


@api_view([
    'GET',
])
def view_users(request):
    if request.method== 'GET':
        user = User.objects.all().values()
        return Response(user,status=200)

@api_view([
    'GET',
])
def view_user(request,id):
    if request.method== 'GET':
        user = User.objects.filter(id=id).values()
        return Response(user[0],status=200)

@api_view([
    'GET',
])
@permission_classes([IsAuthenticated])
def fetch_user(request):
    if request.method== 'GET':
        user = User.objects.get(email=request.user)
        token = Token.objects.get(user=user)
        serializer = serialize_user(user, token)
        return Response(serializer,status=200)

@api_view([
    'POST',
])
@permission_classes([IsAuthenticated])
def change_dp(request):
    if request.method== 'POST':
        user = User.objects.get(email=request.user)
        serializer = serializers.ChangeDpSerializers(user,data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response('Ok',status=200)

@api_view([
    'POST',
])
@permission_classes([IsAuthenticated])
def change_name(request):
    if request.method== 'POST':
        user = User.objects.get(email=request.user)
        user.name=request.data['name']
        user.save()
        return Response('Ok',status=200)

@api_view([
    'POST',
])
def email_check(request):
    if request.method== 'POST':
        user = User.objects.filter(email=request.data['email'])
        if user.exists():
            return Response({'data':'NOTOK','provider':user[0].auth_provider},status=200)
        else:
            return Response('OK',status=200)

@api_view([
    'POST',
])
def phone_check(request):
    if request.method== 'POST':
        user = User.objects.filter(phone=request.data['phone'])
        if user.exists():
            return Response('NOTOK',status=200)
        else:
            return Response('OK',status=200)


@api_view([
    'GET',
])
def phone_otp_generation(request,phone):
    if request.method== 'GET':
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTPPHONE = pyotp.HOTP(key)
        d = PhoneVerifications.objects.filter(phone = phone).delete()
        p = PhoneVerifications.objects.create(phone=phone,otp=OTPPHONE.at(1))
        data = {
            'user': "STRANALYST",
            'password': "13#APR$2021",
            'sid':'SCOUTT',            
            'msisdn': phone,
            'msg':OTPPHONE.at(1)+""" is your OTP for phone verification. For any help, Please contact us at
scoutstack.co.in
8827979008""",
            'fl': 0,
            'gwid': 2,
        }
        
        r = requests.post('https://cloud.smsindiahub.in/vendorsms/pushsms.aspx', params=data)
        print(r.content)
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTPPHONE.at(1)}, status=200)  # Just for demonstration

@api_view([
    'GET',
])
def email_otp_generation(request,email):
    if request.method== 'GET':
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(email).encode())  # Key is generated
        OTPEMAIL = pyotp.HOTP(key)
        b = EmailVerifications.objects.filter(email = email).delete()
        e = EmailVerifications.objects.create(email=email,otp=OTPEMAIL.at(1))
        
        sub = "Email OTP "
        msg = OTPEMAIL.at(1)+" is your OTP for phone verification. For any help, Please contact us at 8827979008"
        f = "24x7analyst@gmail.com"
        to = email
        
        email = EmailMessage(sub,msg,f,[to])
        email.content_subtype = "html"
        EmailThread(email).start()
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTPEMAIL.at(1)}, status=200)  # Just for demonstration


@api_view([
    'POST',
])
def register_otp_verify(request,phone,email):
    if request.method== 'POST':
        p = PhoneVerifications.objects.filter(phone=phone)
        e = EmailVerifications.objects.filter(email=email)
        phoneWrong=True
        emailWrong=True
        if len(p)>0:
            if request.data['phone']==p[0].otp:
                PhoneVerifications.objects.filter(phone = phone).delete()
                phoneWrong=False
        
        if len(e)>0:
            if request.data['email']==e[0].otp:
                EmailVerifications.objects.filter(email = email).delete()
                emailWrong=False

        if not phoneWrong and not emailWrong:
            return Response('OK',status=200)
        elif phoneWrong and emailWrong:
            return Response('Email and Phone OTP are Wrong.',status=400)
        elif phoneWrong and not emailWrong:
            return Response('Phone OTP is Wrong.',status=400)
        elif not phoneWrong and emailWrong:
            return Response('Email OTP is Wrong.',status=400)
        else:     
            return Response("OTP is Wrong", status=400) 
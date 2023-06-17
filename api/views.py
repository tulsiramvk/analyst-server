from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import re
from typing import Dict, Any
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.mail import send_mail, EmailMessage
import threading
import datetime
import base64
import pyotp
import requests
from . import models
from . import serializers
from datetime import timedelta
from auth_user.models import User

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


@api_view([
    'POST',
])
def create_package(request):
    if request.method== 'POST':
        data = {
            'code':request.data['code'],
            'name':request.data['name'],
            'desc':request.data['desc'],
            'creds':request.data['creds'],
            'price':request.data['price'],
        }
        data = models.Package.objects.create(**data)
        res = serializers.serialize_package(data)
        return Response(res,status=200)

@api_view([
    'GET',
])
def view_package(request):
    if request.method== 'GET':
        data = models.Package.objects.values()
        return Response(data,status=200)

# ----------------------Category View------------------------------

@api_view([
    'GET',
])
def view_category(request):
    if request.method== 'GET':
        data = models.Category.objects.values()
        return Response(data,status=status.HTTP_200_OK)
        
@api_view([
    'POST',
])
def create_category(request):
    if request.method== 'POST':
        serializer = serializers.CategorySerialiers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'PUT',
])
def update_category(request,id):
    if request.method== 'PUT':
        d = models.Category.objects.get(id=id)
        serializer = serializers.CategorySerialiers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_category(request,id):
    if request.method== 'DELETE':
        d = models.Category.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)

# ----------------------Product View------------------------------

@api_view([
    'GET',
])
def view_product(request):
    if request.method== 'GET':
        data = models.Product.objects.values()
        return Response(data,status=status.HTTP_200_OK)

@api_view([
    'POST',
])
def create_product(request):
    if request.method== 'POST':
        serializer = serializers.ProductSerialiers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'PUT',
])
def update_product(request,id):
    if request.method== 'PUT':
        d = models.Product.objects.get(id=id)
        serializer = serializers.ProductSerialiers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_product(request,id):
    if request.method== 'DELETE':
        d = models.Product.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)

# ----------------------Packages View------------------------------

@api_view([
    'GET',
])
def view_packages(request):
    if request.method== 'GET':
        data = models.Packages.objects.values()
        return Response(data,status=status.HTTP_200_OK)
        
@api_view([
    'POST',
])
def create_packages(request):
    if request.method== 'POST':
        serializer = serializers.PackagesSerialiers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'PUT',
])
def update_packages(request,id):
    if request.method== 'PUT':
        d = models.Packages.objects.get(id=id)
        serializer = serializers.PackagesSerialiers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_packages(request,id):
    if request.method== 'DELETE':
        d = models.Packages.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)

# --------------------------------------------------------------------------------

# ----------------------Packages View------------------------------

@api_view([
    'POST',
])
@permission_classes([IsAuthenticated])
def create_transactions(request):
    if request.method== 'POST':
        user = User.objects.get(email=request.user)
        gst = format(float(int(request.data['price']) * 18 / 118),'.2f')
        payable_amount= float(int(request.data['price']) - float(gst))
        sgst = format(float(gst)/2, '.2f')
        cgst = format(float(gst)/2, '.2f')
        igst = format(float(gst),'.2f')
        invoice_number = models.InvoiceNumber.objects.all()
        inumber = 0
        if len(invoice_number) > 0:
            inumber = int(invoice_number[0].inumber) + 1
        else:
            inumber = 1

        if request.data['status']=='S':
            data = models.Transactions.objects.create(user_id=user,package=models.Packages.objects.get(id=request.data['package']),product_id=models.Product.objects.get(id=request.data['product']),invoice=None,invoice_number=inumber,
                price=request.data['price'],gst=gst,payable_amount=payable_amount,address=request.data['address'],states=request.data['states'],sgst=sgst,cgst=cgst,igst=igst,
                client_gst=request.data['client_gst'],payment_mode=request.data['payment_mode'],ref_number=request.data['ref_number'],transaction_state='S')
            if data:
                es = models.Services.objects.filter(user=user,product_id=data.product_id,service_state='A')
                if es:
                    es=es.latest('created_at')
                    s = models.Services.objects.create(invoice=data,user=user,product_id=data.product_id,service_type='P',service_state='U',
                    start_date=es.end_date+timedelta(days=1),end_date=es.end_date+timedelta(days=data.package.validity))
                    invoice_number = models.InvoiceNumber.objects.all()
                    invoice_number.delete()
                    models.InvoiceNumber.objects.create(inumber=inumber)
                    return Response('OK',status=status.HTTP_200_OK)
                else:
                    s = models.Services.objects.create(invoice=data,user=user,product_id=data.product_id,service_type='P',service_state='A',
                    start_date=timezone.now().date()+timedelta(days=1),end_date=timezone.now().date()+timedelta(days=data.package.validity))
                    invoice_number = models.InvoiceNumber.objects.all()
                    invoice_number.delete()
                    models.InvoiceNumber.objects.create(inumber=inumber)
                    return Response('OK',status=status.HTTP_200_OK)     
        elif request.data['status']=='F':
            models.Transactions.objects.create(user_id=user,package=models.Packages.objects.get(id=request.data['package']),product_id=models.Product.objects.get(id=request.data['product']),invoice=None,invoice_number=None,
            price=request.data['price'],gst=gst,payable_amount=payable_amount,address=request.data['address'],states=request.data['states'],sgst=sgst,cgst=cgst,igst=igst,
            client_gst=request.data['client_gst'],payment_mode=request.data['payment_mode'],ref_number=request.data['ref_number'],transaction_state='F')
            return Response('Failed',status=400)
        else:
            return Response('Failed',status=400)

@api_view([
    'GET',
])
@permission_classes([IsAuthenticated])
def view_transactions(request):
    if request.method== 'GET':
        user = User.objects.get(email=request.user)
        data = models.Transactions.objects.filter(user_id=user)
        d = serializers.TransactionViewSerialiers(data,many=True)
        return Response(d.data,status=200)

# -------------------------------------Subscription-----------------------

@api_view([
    'GET',
])
@permission_classes([IsAuthenticated])
def view_active_supscription(request):
    if request.method== 'GET':
        user = User.objects.get(email=request.user)
        data = models.Services.objects.filter(user_id=user,service_state='A').order_by('-created_at')
        d = serializers.ServiceSerialiers(data,many=True)
        return Response(d.data,status=200)

@api_view([
    'GET',
])
@permission_classes([IsAuthenticated])
def view_upcoming_subscription(request):
    if request.method== 'GET':
        user = User.objects.get(email=request.user)
        data = models.Services.objects.filter(user_id=user,service_state='U').order_by('-created_at')
        d = serializers.ServiceSerialiers(data,many=True)
        return Response(d.data,status=200)

# ------------------------------------------------------App Banner Work-------------------------------------------------

@api_view([
    'POST',
])
def create_banner(request):
    if request.method== 'POST':
        serializer = serializers.BannerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)

@api_view([
    'GET',
])
def view_banner(request):
    if request.method== 'GET':
        data = models.Banner.objects.values()
        return Response(data,status=200)

@api_view([
    'PUT',
])
def update_banner(request,id):
    if request.method== 'PUT':
        d = models.Banner.objects.get(id=id)
        serializer = serializers.BannerSerializers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_banner(request,id):
    if request.method== 'DELETE':
        d = models.Banner.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)

# ------------------------------------------------------App Support And Resistance Work-------------------------------------------------

@api_view([
    'POST',
])
def create_sar(request):
    if request.method== 'POST':
        serializer = serializers.SarSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)

@api_view([
    'GET',
])
def view_sar(request):
    if request.method== 'GET':
        data = models.Sar.objects.values()
        return Response(data,status=200)

@api_view([
    'PUT',
])
def update_sar(request,id):
    if request.method== 'PUT':
        d = models.Sar.objects.get(id=id)
        serializer = serializers.SarSerializers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_sar(request,id):
    if request.method== 'DELETE':
        d = models.Sar.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)

# ----------------------------Cron Job Work-----------------------------------------

@api_view([
    'GET',
])
def service_update_job(request):
    if request.method== 'GET':
        E = models.Services.objects.filter(service_state='A',end_date__lt=timezone.now().date())
        E.update(service_state='E')
        A = models.Services.objects.filter(service_state='U',start_date__lte=timezone.now().date())
        A.update(service_state='A')
        return Response('Ok')
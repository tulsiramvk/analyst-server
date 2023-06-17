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
import requests
from . import models
from . import serializers
from datetime import timedelta
from auth_user.models import User
from api.models import Services

# -------------------Research Product Work-----------------------

@api_view([
    'POST',
])
def create_research_product(request):
    if request.method== 'POST':
        serializer = serializers.ResearchProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view([
    'GET',
])
def view_research_product(request):
    if request.method== 'GET':
        data = models.Product.objects.values()
        return Response(data,status=200)

@api_view([
    'PUT',
])
def update_research_product(request,id):
    if request.method== 'PUT':
        d = models.Product.objects.get(id=id)
        serializer = serializers.ResearchProductSerializers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_research_product(request,id):
    if request.method== 'DELETE':
        d = models.Product.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)

# -------------------Research Updates Work-----------------------

@api_view([
    'POST',
])
def create_research_updates(request):
    if request.method== 'POST':
        serializer = serializers.ResearchUpdatesSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view([
    'GET',
])
def view_research_updates(request):
    if request.method== 'GET':
        data = models.Updates.objects.values()
        return Response(data,status=200)

@api_view([
    'PUT',
])
def update_research_updates(request,id):
    if request.method== 'PUT':
        d = models.Updates.objects.get(id=id)
        serializer = serializers.ResearchUpdatesSerializers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_research_updates(request,id):
    if request.method== 'DELETE':
        d = models.Updates.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)


# -------------------Research LotSize Work-----------------------

@api_view([
    'POST',
])
def create_lotsize(request):
    if request.method== 'POST':
        d = models.Lotsize.objects.all().delete()
        # 
        serializer = serializers.LotsizeSerializers(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


@api_view([
    'GET',
])
def view_lotsize(request):
    if request.method== 'GET':
        data = models.Lotsize.objects.values()
        return Response(data,status=200)

@api_view([
    'PUT',
])
def update_lotsize(request,id):
    if request.method== 'PUT':
        d = models.Lotsize.objects.get(id=id)
        serializer = serializers.LotsizeSerializers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view([
    'DELETE',
])
def delete_lotsize(request,id):
    if request.method== 'DELETE':
        d = models.Lotsize.objects.get(id=id)
        d.delete()
        return Response('OK', status=status.HTTP_200_OK)

# -------------------Research Expiry Work-----------------------

@api_view([
    'POST',
])
def create_expiry(request):
    if request.method== 'POST':
        d = models.ExpiryDate.objects.all().delete()
        serializer = serializers.ExpirySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view([
    'GET',
])
def view_expiry(request):
    if request.method== 'GET':
        data = models.ExpiryDate.objects.values()
        return Response(data,status=200)

@api_view([
    'PUT',
])
def update_expiry(request,id):
    if request.method== 'PUT':
        d = models.ExpiryDate.objects.get(id=id)
        serializer = serializers.ExpirySerializers(d,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# ------------------------------------------------------------------------------------

@api_view([
    'POST',
])
@permission_classes([IsAuthenticated])
def send_call(request):
    if request.method== 'POST':
        user = User.objects.get(email=request.user)
        state = request.data['state']
        currProduct = request.data['currProduct']
        msgContent = request.data['msgContent']
        data = Services.objects.filter(product_id=currProduct['product_id'],service_state='A')
        calldata = {
            'segmant':currProduct['product_id'],'calls':msgContent,'ct':state['ct'],'owner':user.id,'stock_name':state['stockName'], 'buy_sell':state['type'] if state['type'] else None,
            'call_put':state['option'] if state['option'] else None , 'expiry_date':state['expiryDate'] if state['expiryDate'] else None ,'strike_price':state['strikePrice'] if state['strikePrice'] else None,
            'stockPrice':state['stockPrice'] if state['stockPrice'] else None ,'lotsize':state['lotsize'] if state['lotsize'] else None
        }
        serializer = serializers.CallSerializers(data=calldata)
        if serializer.is_valid():
            serializer.save()
            cc = models.CallsHistory.objects.get(id=serializer.data['id'])
            aList = [models.UserBaseCall(user=i.user,call=cc,callType='C') for i in data]
            models.UserBaseCall.objects.bulk_create(aList)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors,status=400)

@api_view([
    'GET',
])
def fetch_call(request):
    if request.method== 'GET':
        data = models.CallsHistory.objects.values()
        return Response(data,status=200)

@api_view([
    'POST',
])
def send_update(request):
    if request.method== 'POST':
        msgContent = request.data['msgContent']
        data = request.data['data']
        execution = request.data['execution']
        call = models.CallsHistory.objects.get(id=data['id'])
        call = models.CallsHistory.objects.filter(id=data['id']).update(
            update=request.data['currUpdateId'],updates=msgContent,profit_loss=request.data['execution'],update_time=timezone.now()
        )
        dd = models.UserBaseCall.objects.filter(call=call[0].id,callType='C')
        aList = [models.UserBaseCall(user=i.user,call=call,callType='U') for i in dd]
        models.UserBaseCall.objects.bulk_create(aList,ignore_conflicts=True)
        return Response('OK',status=200)

# -----------------------------------App inbox--------------------------------------
@api_view([
    'GET',
])
@permission_classes([IsAuthenticated])
def fetch_inbox(request):
    if request.method== 'GET':
        user = User.objects.get(email=request.user)
        dd = models.UserBaseCall.objects.filter(user=user).order_by('-created_at')
        data = serializers.InboxSerializers(dd)
        return Response(data.data['data'],status=200)

@api_view([
    'GET',
])
@permission_classes([IsAuthenticated])
def fetch_my_call(request):
    if request.method== 'GET':
        user = User.objects.get(email=request.user)
        d = models.UserBaseCall.objects.filter(user=user,callType='C').values_list('call',flat=True)
        data = models.CallsHistory.objects.filter(id__in=d).order_by('-created_at').values()
        return Response(data,status=200)

@api_view([
    'GET',
])
def fetch_today_calls(request):
    if request.method== 'GET':
        data = models.CallsHistory.objects.filter(created_at__date=timezone.now().date(),updates__isnull=False)
        data = list(data.values_list('calls',flat=True))+list(data.values_list('updates',flat=True))
        return Response(data,status=200)
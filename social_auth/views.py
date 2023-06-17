from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import auth_user
from . import serializers
from rest_framework.authtoken.models import Token
from django.utils import timezone

# Create your views here.

@api_view([
    'POST',
])
def google_auth(request):
    if request.method== 'POST':
        serializer = serializers.GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        Token.objects.filter(user=data).delete()
        token = Token.objects.create(user=data)
        data.last_login=timezone.now()
        data.save()
        serializer = auth_user.views.serialize_user(data,token)
        return Response(serializer,status=200)

@api_view([
    'POST',
])
def facebook_auth(request):
    if request.method== 'POST':
        serializer = serializers.FacebookSocialAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data,status=200)
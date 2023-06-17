from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
import os
import requests
import json
from .models import Product,Updates,Lotsize,ExpiryDate,CallsHistory

class ResearchProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ResearchUpdatesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Updates
        fields = '__all__'

class LotsizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lotsize
        fields = '__all__'

class ExpirySerializers(serializers.ModelSerializer):
    class Meta:
        model = ExpiryDate
        fields = '__all__'

class CallSerializers(serializers.ModelSerializer):
    class Meta:
        model = CallsHistory
        fields = '__all__'

class InboxSerializers(serializers.Serializer):
    data = serializers.SerializerMethodField()
    def get_data(self, obj):
        l = []
        for i in obj:
            d=i.call.calls if i.callType=='C' else i.call.updates
            t=i.call.created_at if i.callType=='C' else i.call.update_time
            l.append({
                'id':i.id,'type':i.callType,'msg':d,'created_at':t,'call_id':i.call_id
            })
        return l
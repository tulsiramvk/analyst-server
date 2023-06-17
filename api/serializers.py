from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
import os
import requests
import json
from .models import Category,Product,Packages,Services,Transactions,Banner,Sar
from typing import Dict, Any

class SarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sar
        fields = '__all__'

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class CategorySerialiers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class PackagesSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = '__all__'

class TransactionSerialiers(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'

class TransactionViewSerialiers(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
     )
    package = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )
    product_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )
    invoice = serializers.CharField(max_length=200)
    invoice_number = serializers.CharField(max_length=10)
    price = serializers.CharField(max_length=200)
    gst = serializers.CharField(max_length=50)
    payable_amount = serializers.CharField(max_length=50)
    address = serializers.CharField()
    states = serializers.CharField(max_length=200)
    sgst = serializers.CharField(max_length=100)
    cgst = serializers.CharField(max_length=100)
    igst = serializers.CharField(max_length=100)
    client_gst = serializers.CharField(max_length=100)
    payment_mode = serializers.CharField(max_length=100)
    ref_number = serializers.CharField(max_length=100)
    transaction_state = serializers.CharField(max_length=100)
    created_at = serializers.CharField(max_length=100)


class ServiceSerialiers(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
     )
    invoice = TransactionViewSerialiers(allow_null=True, required=False)
    product_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    service_type = serializers.CharField(max_length=200)
    service_state = serializers.CharField(max_length=200)
    start_date = serializers.CharField(max_length=200)
    end_date = serializers.CharField(max_length=200)
    created_at = serializers.CharField(max_length=100)
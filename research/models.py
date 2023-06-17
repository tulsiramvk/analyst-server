from django.db import models
import uuid
from django.db.models.fields.related import ForeignKey
from auth_user.models import User
from api.models import Product
from django.utils import timezone
import os
import api

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('CASH','cash'),
        ('FUTURE','future'),
        ('OPTION','option')
    )
    CALCULATION_BASE=(
        ('PROFIT','Profit'),
        ('PERCENTAGE','Percentage'),
    )

    u_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=100,null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,unique=True)
    calculation = models.CharField(max_length=20, choices=CALCULATION_BASE)
    tgt_prcnt = models.CharField(max_length=10, null=True, blank=True)
    sl_prcnt = models.CharField(max_length=10, null=True, blank=True)
    profit = models.CharField(max_length=20, null=True, blank=True)
    loss = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Lotsize(models.Model):
    EXP_TYPE=(
        ('WEEKLY','Weekly'),
        ('MONTHLY','Monthly'),
        ('FINNIFTY','Finnifty'),
        ('COMMODITY','Commodity'),
    )
    stock_name = models.CharField(max_length=100, unique=True)
    lotsize = models.CharField(max_length=100,null=True,blank=True)
    date_exp = models.CharField(max_length=20, choices=EXP_TYPE, null=True, blank=True)

    def __str__(self):
        return self.stock_name

class Updates(models.Model):
    EXC_TYPE=(
        ('POSITIVE','positive'),
        ('NEGATIVE','negative'),
    )
    product_category = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=500)
    update_format = models.TextField()
    execution = models.CharField(max_length=50,choices=EXC_TYPE, null=True, blank=True)

    class Meta:
        unique_together = ('product_category', 'title',)

    def __str__(self):
        return self.title

class ExpiryDate(models.Model):
    weekly = models.DateField()
    monthly = models.DateField()
    finnifty = models.DateField()
    commodity = models.DateField()

class CallsHistory(models.Model):   
    segmant = models.ForeignKey(api.models.Product, on_delete=models.CASCADE)
    update = models.ForeignKey(Updates, on_delete=models.SET_NULL, null=True,blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    calls = models.TextField()
    updates = models.TextField(null=True,blank=True)
    stock_name = models.CharField(null=True,blank=True,max_length=100)
    buy_sell = models.CharField(null=True,blank=True,max_length=50)
    call_put = models.CharField(null=True,blank=True,max_length=20)
    expiry_date = models.DateField(blank=True,null=True)
    strike_price = models.CharField(null=True,blank=True,max_length=50)
    ct = models.CharField(null=True,blank=True,max_length=50)
    stockPrice = models.CharField(null=True,blank=True,max_length=20)
    lotsize = models.CharField(null=True,blank=True,max_length=20)
    profit_loss = models.CharField(null=True,blank=True,max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(null=True,blank=True)

class UserBaseCall(models.Model):
    TYPE=(
        ('C','call'),
        ('U','update'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    call = models.ForeignKey(CallsHistory, on_delete=models.CASCADE,null=True)
    callType = models.CharField(max_length=50,choices=TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'call', 'callType'),

# class Bell(models.Model):
#     def path_and_rename(instance, filename):
#         upload_to = 'bell/'
#         ext = filename.split('.')[-1]
#         # get filename
#         if instance.pk:
#             filename = '{}.{}'.format(instance.pk, ext)
#         else:
#             # set filename as random string
#             filename = '{}.{}'.format(uuid.uuid4().hex, ext)
#         # return the whole path to the file
#         return os.path.join(upload_to, filename)
#     f = models.FileField(upload_to=path_and_rename, max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
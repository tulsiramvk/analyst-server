from django.db import models
from auth_user.models import User
import uuid
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Category(models.Model):
    code = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Packages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    validity = models.IntegerField()
    price = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    offer = models.BooleanField(default=False)
    offer_price = models.CharField(max_length=10,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    color = models.CharField(max_length=50,default='green')

# -----------------------------------------------------1----------------------------

class InvoiceNumber(models.Model):
    inumber = models.CharField(max_length=10)

class Transactions(models.Model):
    TRANSACTION_STATE=(
        ('S','success'),
        ('F','fail'),
    )
    u_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    package = models.ForeignKey(Packages, on_delete=models.SET_NULL, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    invoice = models.FileField(upload_to="invoice")
    invoice_number = models.CharField(max_length=50,null=True,unique=True)
    price = models.CharField(max_length=50, null=True)
    gst = models.CharField(max_length=50, null=True)
    payable_amount = models.CharField(max_length=50, null=True)
    address = models.TextField(null=True)
    states = models.CharField(max_length=50,null=True)
    sgst = models.CharField(max_length=50,null=True,blank=True)
    cgst = models.CharField(max_length=50,null=True,blank=True)
    igst = models.CharField(max_length=50,null=True,blank=True)
    client_gst = models.CharField(max_length=50,null=True,blank=True)
    payment_mode = models.CharField(max_length=200,null=True,blank=True)
    ref_number = models.CharField(max_length=200,null=True,blank=True)
    transaction_state = models.CharField(max_length=50, choices=TRANSACTION_STATE,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

class Services(models.Model):
    SERVICE_TYPE=(
        ('P','paid'),
        ('F','freebie'),
    )
    SERVICE_STATE=(
        ('A','active'),
        ('U','upcoming'),
        ('E','expire'),
    )
    u_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    invoice = models.ForeignKey(Transactions,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE)
    service_state = models.CharField(max_length=50, choices=SERVICE_STATE,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

# ----------------------------------------------------Banner Models---------------------------------------------------

class Banner(models.Model):
    banner = models.FileField(upload_to='Banner',null=True,blank=True)
    link = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# ----------------------------------------------------Support and Resistance Models---------------------------------------------------

class Sar(models.Model):
    name = models.CharField(max_length=20)
    r1 = models.CharField(max_length=10)
    r2 = models.CharField(max_length=10)
    s1 = models.CharField(max_length=10)
    s2 = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
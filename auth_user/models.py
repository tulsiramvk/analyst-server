from django.db import models
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from datetime import datetime, timedelta
import uuid
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self ,name,user_type,is_verified,phone,is_active,is_staff,is_superuser, email, password=None):

        if email is None:
            raise TypeError('Users should have a Email.')
        user = self.model(name=name,email_verify=False,user_type=user_type,is_verified=is_verified,phone=phone,is_active=is_active,is_staff=False,is_superuser=False,email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(name='Admin',user_type='ADMIN',email=email, password=password,phone=None,is_active=True,is_staff=True,is_superuser=True,is_verified=True)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):

    AUTH_PROVIDERS = {'facebook':'facebook','google':'google','email':'email'}

    user_type = models.CharField(max_length=100,null=True)
    u_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone = models.CharField(max_length=12, null=True,unique=True)
    password = models.CharField(max_length=1500,)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    proimg = models.FileField(upload_to='profileImg',null=True)
    auth_provider = models.CharField(max_length=255,blank=False,null=False,default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

class PhoneVerifications(models.Model):
    phone = models.CharField(max_length=13,unique=True)
    otp = models.CharField(max_length=10)

class EmailVerifications(models.Model):
    email = models.CharField(max_length=100,unique=True)
    otp = models.CharField(max_length=10)
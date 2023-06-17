from django.contrib.auth import authenticate
from auth_user.models import User
import os
import random
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_SECRET'))

            return registered_user

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider+'.')

    else:
        user = {
            'name':name,
            'email': email,
            'password': os.environ.get('SOCIAL_SECRET')
            }
        user = User.objects.create(name=name,email=email,auth_provider=provider,user_type='CLIENT')
        user.set_password(os.environ.get('SOCIAL_SECRET'))        
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return new_user
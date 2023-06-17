from google.auth.transport import requests
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_user_phone_number(access_token):
    credentials = Credentials.from_authorized_user_info(info={'access_token': access_token})
    people_service = build('people', 'v1', credentials=credentials)
    user_profile = people_service.people().get(resourceName='people/me', personFields='phoneNumbers').execute()
    phone_number = None
    if 'phoneNumbers' in user_profile:
        phone_number = user_profile['phoneNumbers'][0]['value']
    return phone_number

class Google:

    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except:
            return "The token is either invalid or has expired."
# from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
import requests
import os


class TempUser:
    """ Temporal User used to pass
        authentication (IsAuthenticated)
    """
    def __init__(self, data):
        self.id = data.get('user_id', None)
    
    def is_authenticated(self):
        return True


verify_token_path = '/api/token/verify/'
users_service_hostname = os.getenv('USERS_SERVICE_URL')
verify_token_url = users_service_hostname + verify_token_path


class UsersServiceAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # django adds "HTTP_" to headers
        jwt = request.META.get("HTTP_AUTHORIZATION")
        if not jwt:
            return None
        try:
            jwt = jwt[7:] # get rid of the bearer portion (not safe)
            body = { "token": jwt }
            res = requests.post(verify_token_url, json=body)
            res.raise_for_status()
            data = res.json()
            user = TempUser(data)
        except requests.exceptions.HTTPError as err:
            raise exceptions.AuthenticationFailed('JWT not valid')
        except:
            raise exceptions.AuthenticationFailed('Wrong Token format')
        
        return (user, None)

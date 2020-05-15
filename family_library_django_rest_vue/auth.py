import datetime
import json 

from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
from django.http import HttpResponseBadRequest, JsonResponse

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

import jwt

from .settings import SECRET_KEY


class JWTAuth(BaseAuthentication):
    usermodel = get_user_model()

    def authenticate(self, request):
        try:
            encoded_token = request.META['HTTP_AUTHORIZATION']
            decoded = self.decode_token(encoded_token)
            user = self.get_user_from_token(decoded)
            return (user, None)
        except:
            raise exceptions.AuthenticationFailed('Client not authorized')
        return None
    
    def decode_token(self, encoded_token):
        return jwt.decode(encoded_token, SECRET_KEY, algorithms=['HS256'])

    def get_user_from_token(self, decoded):
        return self.usermodel.objects.get(email=decoded['username'])


@require_POST
def auth_jwt(request):
    try:
        # get username and passsword
        data = json.loads(request.body.decode())
        username = data['username']
        password = data['password']
        # authenticate user credentials
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # create token good for 24 hours
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1)
            token = jwt.encode({'username': user.username, 'exp': expiration_date}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'token': str(token)})
        else:
            return HttpResponseBadRequest('bad user info')
    except Exception as e:
        return HttpResponseBadRequest(e)

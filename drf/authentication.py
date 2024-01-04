from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
import time
from drf.settings import INVALID_TIME


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('token', None)
        if not token:
            raise exceptions.NotAuthenticated(
                {
                    'error': 'Authentication failed',
                    'message': 'Authentication token not supplied',
                    'status': 401
                })
        obj = Token.objects.filter(key=token).first()
        current_time = int(time.time())
        created = int(obj.created.timestamp())
        if current_time - created > INVALID_TIME:
            raise exceptions.AuthenticationFailed(
                {
                    'error': 'Authentication failed',
                    'message': 'Token expired',
                    'status': 401,
                    'expired_at': created + INVALID_TIME,
                }
            )
        obj.token = token
        obj.save()

        if not obj:
            raise exceptions.AuthenticationFailed(
                {
                    'error': 'Authentication failed',
                    'message': 'Authentication is illegal',
                    'status': 401,
                }
            )
        else:
            return obj, obj.user

    def authenticate_header(self, request):
        return 'Authentication Failed'

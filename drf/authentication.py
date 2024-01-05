from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


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

        if token != cache.get('token'):
            raise exceptions.NotAuthenticated(
                {
                    'error': 'Authentication failed',
                    'message': 'Authentication token is invalid',
                    'status': 401
                }
            )
        else:
            return (token, None)

    def authenticate_header(self, request):
        return 'Authentication Failed'

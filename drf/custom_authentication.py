from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import User


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 获取请求头中的认证信息，例如Token
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None
        # 进行认证逻辑，例如解析Token，检查用户是否存在等
        # 在此简单示例中，我们使用Token中的字符串作为用户名，创建一个虚拟的用户对象
        _, token = auth_header.split(' ')
        username = token
        user = User(username=username)
        if not user:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return user, None

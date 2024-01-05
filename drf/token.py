import jwt
import datetime
from django.conf import settings


def generate_token(username):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(days=1)  # 设置token有效期为1天
    payload = {
        "iss": "Online JWT Builder",
        "aud": "https://gitee.com/joyamon/drf.git",
        'exp': int(expiry.timestamp()),
        'username': username,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

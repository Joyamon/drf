from django.test import TestCase
from rest_framework.test import CoreAPIClient

# Create your tests here.
client = CoreAPIClient()
schema = client.get('http://127.0.0.1:8000/user/captcha/')
print(schema)
from __future__ import absolute_import, unicode_literals
# import eventlet
# eventlet.monkey_patch()
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')
app = Celery('drf', broker_connection_retry_on_startup=True)
# namespace='CELERY'作用是允许你在Django配置文件中对Celery进行配置
# 但所有Celery配置项必须以CELERY开头，防止冲突
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

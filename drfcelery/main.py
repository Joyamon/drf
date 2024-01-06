# 主程序
import os
from celery import Celery
app = Celery("drf_task", include=['drfcelery.drf_task.tasks'])  # include参数必须有，不然找不到任务
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')
app.config_from_object("drfcelery.config")
app.autodiscover_tasks(["drfcelery.drf_task.tasks"])

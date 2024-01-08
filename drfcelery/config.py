broker_url = 'redis://127.0.0.1:6379/10'
result_backend = 'redis://127.0.0.1:6379/11'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True

imports = ('drfcelery.drf_task',)

from celery.schedules import crontab
from .main import app

# 定时任务的调度列表，用于注册定时任务
app.conf.beat_schedule = {
    'schedule_test': {
        'task': 'drfcelery.drf_task.tasks.run_test',
        'schedule': crontab(minute='52', hour='10'),
    },

}

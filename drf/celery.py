import os
from celery import platforms
from celery import Celery
from django.utils import timezone

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')

app = Celery("drf")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#  should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.now = timezone.now
app.autodiscover_tasks(['drfUser.tasks'])

platforms.C_FORCE_ROOT = True

# 重写CustomScheduler 方法，改为东八区
from celery.beat import Scheduler, ScheduleEntry, event_t
from celery.utils.log import get_logger


class CustomScheduler(Scheduler):
    def __init__(self, *args, **kwargs):
        kwargs['scheduler_cls'] = 'django_celery_beat.schedulers:TimezoneScheduler'
        super().__init__(*args, **kwargs)

    def _now(self):
        return timezone.now()


app.conf.beat_scheduler = 'drf.celery.CustomScheduler'

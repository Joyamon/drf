# Create your tasks here
from celery import shared_task


@shared_task
def run_test():
    print("测试任务开始执行.....")

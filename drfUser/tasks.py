from celery import shared_task


@shared_task
def run_test_task():
    print("这是测试任务")

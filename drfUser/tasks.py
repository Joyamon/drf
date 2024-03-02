from celery import shared_task


@shared_task
def run_test_task():
    print("this is test task")

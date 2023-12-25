# Create your tasks here
from celery import shared_task


@shared_task
def run_test():
    print("Running test")

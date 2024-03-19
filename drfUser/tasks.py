from celery import shared_task


@shared_task
def run_test_task():
    print("这是测试任务,正在运行...")

@shared_task
def run_router_one():
    print("这是路由一,正在运行...")

@shared_task
def run_router_two():
    print("这是路由二,正在运行...")



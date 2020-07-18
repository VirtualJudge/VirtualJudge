from celery import shared_task


@shared_task
def add(x, y):
    print( x + y)


@shared_task
def mul(x, y):
    print(x * y)

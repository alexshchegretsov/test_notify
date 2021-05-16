from celery import Celery

# Celery settings
BROKER_URL = 'redis://localhost:6379/1'
BACKEND_URL = 'redis://localhost:6379/1'
ACCEPT_CONTENT = ['json', ]

celery = Celery('celery_tasks', broker=BROKER_URL, backend=BACKEND_URL)


@celery.task
def foo(data):
    print(data)

    with open('foo.txt', 'a') as f:
        f.write(data)


@celery.task
def boo(data):
    with open('boo.txt', 'a') as f:
        f.write(data)

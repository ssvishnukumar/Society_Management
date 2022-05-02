
import os

from celery import Celery

from django.conf import settings

# from user_login.task import send_notification
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SC.settings')

app = Celery('SC')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


"""app.conf.beat_schedule = {
    'scheduled_task' : {
        'task' : 'user_login.task.add',
        'schedule': 5.0,
        'args': (4,5),
    },
}"""


# @app.task(bind=True)
# def debug_task(self):
#     print('Hellow CELERY...')
    
# @app.task
# def test_task():
#     print("This is the Test Task...")

# app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

# if the above one is not working...use the below one.
# from django.apps import apps
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

#for scheduling

# app.conf.beat_schedule = {
#     'add-every-2-hour' : {
#         'task' : 'send_notification',
#         'schedule' : crontab(minute='*/1'),
#     }
# }


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')




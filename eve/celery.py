import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eve.settings')
app = Celery('update_api_rates')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# BEAT TASKS

app.conf.beat_schedule = {
    'check-every-hour': {
        'task': 'tasks.update_star_db',
        'schedule': crontab(minute='*'),
    },
}
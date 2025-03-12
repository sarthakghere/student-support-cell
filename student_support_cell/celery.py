import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_support_cell.settings')

app = Celery('student_support_cell')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Kolkata'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
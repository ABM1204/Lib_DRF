from __future__ import absolute_import, unicode_literals

from celery import Celery
from django.conf import settings

app = Celery('library')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

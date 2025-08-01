from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece la configuración por defecto de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

# Carga configuración de Django con prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Detecta tasks.py en cada app registrada en INSTALLED_APPS
app.autodiscover_tasks()

# Optional: define task para debug
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

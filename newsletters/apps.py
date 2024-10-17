import os
from django.apps import AppConfig
from django.conf import settings


class NewslettersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletters'


    def ready(self):
        if settings.DEBUG and os.environ.get('RUN_MAIN') == 'true':
            from newsletters.task import scheduler
            scheduler.start()





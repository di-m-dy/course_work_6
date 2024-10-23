import os
from time import sleep

from django.apps import AppConfig
from config.settings import AUTORUN_SCHEDULER, DEBUG


class NewslettersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletters'


    def ready(self):
        if DEBUG and os.environ.get('RUN_MAIN') and AUTORUN_SCHEDULER:
            from newsletters.task import scheduler
            sleep(2)
            scheduler.start() # автоматический запуск периодической задачи (отправка рассылок) при запуске приложения

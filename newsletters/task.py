from time import timezone
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from config.settings import ZONE
from newsletters.models import Newsletter, NewsletterReport
from newsletters.services import send_newsletter, update_next_send

END_DELTA = timedelta(seconds=60)


def send():
    now = datetime.now(ZONE)

    active_newsletters = Newsletter.objects.filter(status='active')
    closed_newsletters = Newsletter.objects.filter(status='closed', period__in=['days', 'weeks', 'months'])
    for newsletter in active_newsletters:
        reports = NewsletterReport.objects.filter(newsletter=newsletter)
        if reports:
            last_report = reports.order_by('-date_time').first()
            if now >= last_report.next_send:
                    send_newsletter(newsletter=newsletter)
        else:
            if now >= newsletter.date_time:
                send_newsletter(newsletter=newsletter)
                if newsletter.period == 'once':
                    newsletter.status = 'closed'
                    newsletter.save()

    for newsletter in closed_newsletters:
        reports = NewsletterReport.objects.filter(newsletter=newsletter)
        if reports:
            last_report = reports.order_by('-date_time').first()
            if now >= last_report.next_send:
                update_next_send(last_report)


# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# Добавление задачи на выполнение каждую минуту
scheduler.add_job(send, 'interval', seconds=10, id='mailing_task', replace_existing=True)

from time import timezone
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from config.settings import TIME_ZONE
from newsletters.models import Newsletter, NewsletterReport
from newsletters.services import send_newsletter

END_DELTA = timedelta(seconds=60)
PERIOD_DELTA = {
    'days': timedelta(hours=24),
    'weeks': timedelta(days=7),
    'months': timedelta(days=30)
}

def send():
    # Текущая дата и время
    zone = pytz.timezone(TIME_ZONE)
    now = datetime.now(zone)
    late_newsletters = Newsletter.objects.filter(date_time__lt=now - END_DELTA).filter(status='active').filter(period='once')
    for newsletter in late_newsletters:
        NewsletterReport.objects.create(
            newsletter=newsletter,
            is_success=False,
            report='Рассылка просрочена'
        )
        newsletter.status = 'closed'
        newsletter.save()

    active_newsletters = Newsletter.objects.filter(status='active')
    for newsletter in active_newsletters:
        reports = NewsletterReport.objects.filter(newsletter=newsletter)
        if reports:
            last_report = reports.order_by('-date_time').first()
            if newsletter.period in ['days', 'weeks', 'months']:
                next_sending = PERIOD_DELTA[newsletter.period] + last_report.date_time
                if next_sending < now < next_sending + END_DELTA:
                    send_newsletter(newsletter=newsletter)
        else:
            if newsletter.period == 'once':
                if newsletter.date_time < now < newsletter.date_time + END_DELTA:
                    send_newsletter(newsletter=newsletter)
                    newsletter.status = 'closed'
                    newsletter.save()
            else:
                next_sending = newsletter.date_time
                if next_sending < now < next_sending + END_DELTA:
                    send_newsletter(newsletter=newsletter)


# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# Добавление задачи на выполнение каждую минуту
scheduler.add_job(send, 'interval', seconds=10, id='mailing_task', replace_existing=True)

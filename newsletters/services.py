import smtplib
from datetime import timedelta

from django.core.mail import send_mail
from django.utils.datetime_safe import datetime

from config.settings import EMAIL_HOST_USER, ZONE
from newsletters.models import Newsletter, NewsletterReport

PERIOD_DELTA = {
        'days': timedelta(hours=24),
        'weeks': timedelta(days=7),
        'months': timedelta(days=30)
    }


def send_newsletter(newsletter: Newsletter):

    try:
        send = send_mail(
            subject=newsletter.message.title,
            message=newsletter.message.text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[i.email for i in newsletter.clients.all()],
            fail_silently=False
        )
        NewsletterReport.objects.create(
            newsletter=newsletter,
            is_success=bool(send),
            next_send=datetime.now(ZONE) + PERIOD_DELTA[newsletter.period] if newsletter.period != 'once' else None
        )
    except smtplib.SMTPException as e:
        NewsletterReport.objects.create(
            newsletter=newsletter,
            is_success=False,
            report=e
        )
    except Exception as e:
        NewsletterReport.objects.create(
            newsletter=newsletter,
            is_success=False,
            report=e
        )

def update_next_send(report: NewsletterReport):
    report.next_send = datetime.now(ZONE) + PERIOD_DELTA[newsletter.period]
    report.save()


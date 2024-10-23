import smtplib
from datetime import timedelta

from django.core.mail import send_mail
from django.utils.datetime_safe import datetime
from django.views.decorators.cache import cache_page

from config.settings import EMAIL_HOST_USER, ZONE, CACHED_ENABLED
from newsletters.models import Newsletter, NewsletterReport

# интервалы рассылок для разных периодов
PERIOD_DELTA = {
        'days': timedelta(hours=24),
        'weeks': timedelta(days=7),
        'months': timedelta(days=30)
    }


def send_newsletter(newsletter: Newsletter, no_report=False):
    """
    Отправка рассылок
    no_report: не сохраняет в базу отчеты
    """
    try:
        send = send_mail(
            subject=newsletter.message.title,
            message=newsletter.message.text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[i.email for i in newsletter.clients.all()],
            fail_silently=False
        )
        if no_report:
            print('Success!')
        else:
            NewsletterReport.objects.create(
                newsletter=newsletter,
                is_success=bool(send),
                next_send=datetime.now(ZONE) + PERIOD_DELTA[newsletter.period] if newsletter.period != 'once' else None
            )
    except smtplib.SMTPException as e:
        if no_report:
            print(f"Error: {e}")
        else:
            NewsletterReport.objects.create(
                newsletter=newsletter,
                is_success=False,
                report=e
            )
    except Exception as e:
        if no_report:
            print(f"Error: {e}")
        else:
            NewsletterReport.objects.create(
                newsletter=newsletter,
                is_success=False,
                report=e
            )

def update_next_send(report: NewsletterReport):
    """
    Обновляет время следующей отправки (для приостановленных рассылок)
    """
    report.next_send = datetime.now(ZONE) + PERIOD_DELTA[report.newsletter.period]
    report.save()


def set_cache_controller(controller):
    """
    Кэширование контроллера
    :param controller: контроллер Controller.as_view()
    """
    if CACHED_ENABLED:
        return cache_page(200)(controller)
    return controller

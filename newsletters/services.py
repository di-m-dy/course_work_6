import smtplib
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from newsletters.models import Newsletter, NewsletterReport


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
            is_success=bool(send)
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

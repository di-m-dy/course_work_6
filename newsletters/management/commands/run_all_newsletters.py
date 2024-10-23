from django.core.management import BaseCommand
from newsletters.models import Newsletter
from newsletters.services import send_newsletter

class Command(BaseCommand):
    """
    Отправка всех рассылок в ручном режиме
    """
    def handle(self, *args, **options):
        newsletters = Newsletter.objects.all()
        for newsletter in newsletters:
            send_newsletter(newsletter, no_report=True)

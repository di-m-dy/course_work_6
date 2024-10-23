from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Команда для создания простого пользователя
        """
        user = User.objects.create(
            email='simple_user@example.com',
            first_name='Simple',
            last_name='User'
        )
        user.set_password('qwerasdf')
        user.save()

from django.contrib.auth.models import Permission, Group
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        permission_code_names = (
            'view_owner_newsletter',
            'view_list_user',
            'set_isactive_user',
            'set_closed_newsletter',
            'add_blog',
            'change_blog',
            'delete_blog',
            'view_blog'
        )
        permissions = Permission.objects.filter(codename__in=permission_code_names).all()
        group, created = Group.objects.get_or_create(name='manager')
        for permission in permissions:
            group.permissions.add(permission)
        user = User.objects.create(
            email='manager@example.com',
            first_name='Manager',
            last_name='Manager Newsletters Service'
        )
        user.groups.add(group)
        user.set_password('0987')
        user.save()

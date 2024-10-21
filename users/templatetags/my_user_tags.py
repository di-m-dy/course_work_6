from django import template

register = template.Library()


@register.filter(name='manager')
def manager(user):
    group_list = [
        'manager'
    ]
    return user.groups.filter(name__in=group_list).exists() or user.is_superuser

from django.contrib import admin
from newsletters.models import Newsletter, NewsletterReport, Client, Message

admin.site.register(Client)
admin.site.register(Newsletter)
admin.site.register(NewsletterReport)
admin.site.register(Message)



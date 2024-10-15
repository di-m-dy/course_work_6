from django.urls import path
from newsletters.views import NewsletterListView, MessageListView, NewsletterDetailView, NewsletterCreateView

app_name = 'newsletters'

urlpatterns = [
    path('newsletters', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/add', NewsletterCreateView.as_view(), name='add_newsletter'),
    path('messages', MessageListView.as_view(), name='message_list')
]

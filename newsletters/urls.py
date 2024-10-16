from django.urls import path
from newsletters.views import (NewsletterListView,
                               MessageListView,
                               NewsletterDetailView,
                               NewsletterCreateView,
                               NewsletterUpdateView,
                               NewsletterDeleteView,
                               MessageDetailView,
                               MessageCreateView,
                               MessageUpdateView,
                               MessageDeleteView,
                               ClientListView, ClientCreateView, ClientUpdateView)

app_name = 'newsletters'

urlpatterns = [
    path('newsletters', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/add', NewsletterCreateView.as_view(), name='add_newsletter'),
    path('newsletters/update/<int:pk>', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('newsletters/delete/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('messages', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('messages/add', MessageCreateView.as_view(), name='add_message'),
    path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('clients', ClientListView.as_view(), name='client_list'),
    path('clients/add', ClientCreateView.as_view(), name='add_client'),
    path('clients/update/<int:pk>', ClientUpdateView.as_view(), name='update_client')
]

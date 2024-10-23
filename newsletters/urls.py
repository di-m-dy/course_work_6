from django.urls import path
from newsletters.services import set_cache_controller
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
                               ClientListView,
                               ClientCreateView,
                               ClientUpdateView,
                               NewsletterReportListView,
                               start_sending,
                               stop_sending,
                               HomeListView,
                               ManagerUserListView,
                               DatetimeLateTemplateView,
                               ClientDeleteView)

app_name = 'newsletters'

urlpatterns = [
    path('', set_cache_controller(HomeListView.as_view()), name='home'),
    path('manager/users', ManagerUserListView.as_view(), name='manager_user_list'),
    path('newsletters', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletters/<int:pk>', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletters/<int:newsletter_id>/report', NewsletterReportListView.as_view(), name='newsletter_report'),
    path('newsletters/<int:newsletter_id>/start_sending', start_sending, name='start_sending'),
    path('newsletters/<int:newsletter_id>/stop_sending', stop_sending, name='stop_sending'),
    path('newsletters/add', NewsletterCreateView.as_view(), name='add_newsletter'),
    path('newsletters/update/<int:pk>', NewsletterUpdateView.as_view(), name='update_newsletter'),
    path('newsletters/delete/<int:pk>', NewsletterDeleteView.as_view(), name='delete_newsletter'),
    path('newsletters/<int:newsletter_id>/datetime_late', DatetimeLateTemplateView.as_view(), name='datetime_late'),
    path('messages', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('messages/add', MessageCreateView.as_view(), name='add_message'),
    path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='update_message'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='delete_message'),
    path('clients', ClientListView.as_view(), name='client_list'),
    path('clients/add', ClientCreateView.as_view(), name='add_client'),
    path('clients/update/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('clients/delete/<int:pk>', ClientDeleteView.as_view(), name='delete_client')
]

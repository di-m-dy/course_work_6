from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from users.views import RegisterCreateView, email_verification, reset_password, ProfileUpdateView, Login, logout_confirm

app_name = 'users'

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('logout_confirm', logout_confirm, name='logout_confirm'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('register', RegisterCreateView.as_view(), name='register'),
    path('check_email/<str:token>', email_verification, name='email_verification'),
    path('reset_password', reset_password, name='reset_password'),
    path('profile', ProfileUpdateView.as_view(), name='profile')
]

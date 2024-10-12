from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

# from user.views import RegisterCreateView, email_verification, reset_password, ProfileUpdateView

app_name = 'user'

urlpatterns = [
    path('', LoginView.as_view(template_name='user/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', RegisterCreateView.as_view(), name='register'),
    # path('check_email/<str:token>/', email_verification, name='email_verification'),
    # path('reset_password', reset_password, name='reset_password'),
    # path('profile', ProfileUpdateView.as_view(), name='profile')
]

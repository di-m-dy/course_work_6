import secrets
import string
import random

from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, ProfileForm, LoginForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, TemplateView, RedirectView
from django.contrib.auth.views import LoginView
from users.models import User


class RegisterCreateView(CreateView):
    """
    Регистрация пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/check_email/{token}"
        send_mail(
            subject='Подвтердите регистрацию на сайте',
            message=f"Чтобы подтвердить регистрацию, пройдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class ProfileUpdateView(UpdateView):
    """
    Редактирование пользователя
    """
    model = User
    context_object_name = 'user'
    success_url = reverse_lazy('users:profile')
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class Login(LoginView):
    """
    Логин пользователя
    """
    form_class = LoginForm
    template_name = 'users/login.html'


def email_verification(request, token):
    """
    Верификация по почте
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def reset_password(request):
    """
    Сброс пароля
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        check = User.objects.filter(email=email).exists()
        if check:
            user = User.objects.get(email=email)
            letters = string.ascii_letters  # Заглавные и строчные буквы
            digits = string.digits  # Цифры
            special_chars = string.punctuation  # Специальные символы
            all_chars = letters + digits + special_chars
            password = ''.join(random.choice(all_chars) for _ in range(8))
            user.set_password(password)
            user.save()
            send_mail(
                subject="Сброс пароля",
                message=f"Пароль сброшен. Ваш новый ременный пароль: {password}",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email]
            )
            return render(request, 'users/success_reset_password.html')
        else:
            return render(request, 'users/error_reset_password.html')
    return render(request, 'users/reset_password.html')

def logout_confirm(request):
    return render(request, 'users/logout_confirm.html')


class DeactivateUser(RedirectView):
    """
    Для менеджера - банить пользователя
    """
    pattern_name = 'newsletters:manager_user_list'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        user.is_active = False
        user.save()
        return super().get(request, *args)

class ActivateUser(RedirectView):
    """
    Для менеджера - разбанить пользователя
    """
    pattern_name = 'newsletters:manager_user_list'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        user.is_active = True
        user.save()
        return super().get(request, *args)

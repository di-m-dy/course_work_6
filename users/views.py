import secrets
import string
import random

from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse

from config.settings import EMAIL_HOST_USER
from user.forms import UserRegisterForm, ProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView

from user.models import User


class RegisterCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/check_email/{token}"
        send_mail(
            subject='Подвтердите регистрацию на сайте',
            message=f"Чтобы подтвердить регистрацию, пройдите по ссылке: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class ProfileUpdateView(UpdateView):
    model = User
    context_object_name = 'user'
    success_url = reverse_lazy('catalog:index')
    template_name = 'user/profile.html'
    form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('user:login'))


def reset_password(request):
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
            return render(request, 'user/success_reset_password.html')
        else:
            return render(request, 'user/error_reset_password.html')
    return render(request, 'user/reset_password.html')

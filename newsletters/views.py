from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView
from blog.models import Blog
from config.settings import ZONE
from newsletters.forms import NewsletterForm, MessageForm, ClientForm
from newsletters.models import Newsletter, Message, Client, NewsletterReport
from users.models import User



class CheckManager(UserPassesTestMixin):
    """
    Миксин проверяет: является ли пользователь менеджером
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists()

class CheckSimpleUserCreate(UserPassesTestMixin):
    """
    Миксин проверяет: является ли пользователь простым пользователем
    """
    def test_func(self):
        check_is_not_manager = (not self.request.user.is_superuser and
                            not self.request.user.groups.filter(name='manager').exists())

        return check_is_not_manager

class CheckOwnerUpdateNewsletter(UserPassesTestMixin):
    """
    Миксин проверяет: является ли пользователь простым пользователем
    """
    def test_func(self):
        newsletter = get_object_or_404(Newsletter, pk=self.kwargs.get('pk'))
        return newsletter.user == self.request.user

class CheckOwnerUpdateMessage(UserPassesTestMixin):
    """
    Миксин проверяет: является ли пользователь простым пользователем
    """
    def test_func(self):
        message = get_object_or_404(Message, pk=self.kwargs.get('pk'))
        return message.user == self.request.user

class CheckOwnerUpdateClient(UserPassesTestMixin):
    """
    Миксин проверяет: является ли пользователь простым пользователем
    """
    def test_func(self):
        client = get_object_or_404(Client, pk=self.kwargs.get('pk'))
        return client.user == self.request.user

class CheckOwnerViewNewsletter(PermissionRequiredMixin):
    """
    Миксин проверяет что текущий пользователь является владельцем рассылки
    Или у пользователя есть права просматривать чужие рассылки
    """
    permission_required = 'newsletters.view_owner_newsletter'

    def has_permission(self):
        newsletter = get_object_or_404(Newsletter, pk=self.kwargs.get('pk'))
        return super().has_permission() or newsletter.user == self.request.user


class ManagerUserListView(CheckManager, ListView):
    """
    Отображение списка всех пользователей для менеджера
    """
    model = User
    context_object_name = 'users'
    template_name = 'newsletters/manager_user_list.html'

    def get_queryset(self):
        data = [user for user in User.objects.all() if not user.is_superuser and not user.groups.filter(name='manager').exists()]
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['users'] = [
            {
                'user': item,
                'newsletters': Newsletter.objects.filter(user=item),
                'clients': Client.objects.filter(user=item)
            }
            for item in data['users']
        ]
        return data

class HomeListView(LoginRequiredMixin, TemplateView):
    """
    Главная страница
    """
    model = Newsletter
    template_name = 'newsletters/home.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            return redirect(reverse_lazy('newsletters:manager_user_list'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        user = self.request.user
        newsletters = Newsletter.objects.filter(user=user)
        data['newsletters'] = newsletters
        clients = Client.objects.filter(user=user)
        data['clients'] = clients
        active_newsletters = newsletters.filter(status='active')
        data['active_newsletters'] = active_newsletters
        posts = Blog.objects.filter(is_active=True).order_by('-views_count')[:3]
        data['posts'] = posts
        return data


class NewsletterListView(LoginRequiredMixin, ListView):
    """
    Отображение списка рассылок
    """
    model = Newsletter
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            data = Newsletter.objects.all().order_by('-created_at')
            if self.request.GET.get('user'):
                user = get_object_or_404(User, pk=self.request.GET.get('user'))
                data = data.filter(user=user).order_by('-created_at')
        else:
            data = Newsletter.objects.filter(user=user).order_by('-created_at')
        return data


class NewsletterDetailView(CheckOwnerViewNewsletter, DetailView):
    """
    Отображение информации о рассылке
    """
    model = Newsletter
    context_object_name = 'newsletter'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['reports'] = NewsletterReport.objects.filter(newsletter=self.object)
        if self.object.status == 'created' or (self.object.status == 'closed' and self.object.period != 'once'):
            data['run_send'] = 'start'
        elif self.object.status == 'active':
            data['run_send'] = 'stop'
        else:
            data['run_send'] = None
        return data


class NewsletterCreateView(CheckSimpleUserCreate, CreateView):
    """
    Создание рассылок
    """
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletters:newsletter_list')

    def get_form_kwargs(self):
        """
        Переопределяем метод для передачи текущего пользователя в форму.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Сохраняем форму и перенаправляем пользователя.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class NewsletterUpdateView(CheckOwnerUpdateNewsletter, UpdateView):
    """
    Редактирование рассылок.
    """
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletters:newsletter_list')

    def get_form_kwargs(self):
        """
        Переопределяем метод для передачи текущего пользователя в форму.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Сохраняем форму и перенаправляем пользователя.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class NewsletterDeleteView(CheckOwnerUpdateNewsletter, DeleteView):
    """
    Удаление рассылок.
    """
    model = Newsletter
    success_url = reverse_lazy('newsletters:newsletter_list')


class MessageListView(LoginRequiredMixin, ListView):
    """
    Отображение списка сообщений
    """
    model = Message
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            data = Message.objects.all().order_by('title')
            if self.request.GET.get('user'):
                user = get_object_or_404(User, pk=self.request.GET.get('user'))
                data = data.filter(user=user).order_by('title')
        else:
            data = Message.objects.filter(user=user).order_by('title')
        return data


class MessageDetailView(DetailView):
    """
    Отображение сообщения
    """
    model = Message


class MessageCreateView(CheckSimpleUserCreate, CreateView):
    """
    Создание сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletters:message_list')

    def form_valid(self, form):
        """
        Сохраняем форму и перенаправляем пользователя.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class MessageUpdateView(CheckOwnerUpdateMessage, UpdateView):
    """
    Редактирование сообщения
    """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletters:message_list')

    def form_valid(self, form):
        """
        Сохраняем форму и перенаправляем пользователя.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class MessageDeleteView(CheckOwnerUpdateMessage, DeleteView):
    """
    Удаление сообщения
    """
    model = Message
    success_url = reverse_lazy('newsletters:message_list')


class ClientListView(LoginRequiredMixin, ListView):
    """
    Отображение списка клиентов
    """
    model = Client
    paginate_by = 30

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            data = Client.objects.all().order_by('-created_at')
            if self.request.GET.get('user'):
                user = get_object_or_404(User, pk=self.request.GET.get('user'))
                data = data.filter(user=user).order_by('-created_at')
        else:
            data = Client.objects.filter(user=user).order_by('-created_at')
        if self.request.GET.get('newsletter'):
            newsletter = get_object_or_404(Newsletter, pk=self.request.GET.get('newsletter'))
            data = newsletter.clients.all()
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        if self.request.GET.get('newsletter'):
            data['get_newsletter'] = f"Рассылка #{self.request.GET.get('newsletter')}"
        return data


class ClientCreateView(LoginRequiredMixin, CheckSimpleUserCreate, CreateView):
    """
    Добавление клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletters:client_list')

    def form_valid(self, form):
        """
        Сохраняем форму и перенаправляем пользователя.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, CheckOwnerUpdateClient, UpdateView):
    """
    Редактирование клиента
    """
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletters:client_list')

    def form_valid(self, form):
        """
        Сохраняем форму и перенаправляем пользователя.
        """
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ClientDeleteView(CheckOwnerUpdateClient, DeleteView):
    """
    Удаление клиента
    """
    model = Client
    success_url = reverse_lazy('newsletters:client_list')


class NewsletterReportListView(LoginRequiredMixin, ListView):
    """
    Отображение списка отчетов рассылки
    """
    model = NewsletterReport
    paginate_by = 30

    def get_queryset(self):
        newsletter_id = self.kwargs.get('newsletter_id')
        newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
        data = NewsletterReport.objects.filter(newsletter=newsletter).order_by('-date_time')
        return data

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        newsletter_id = self.kwargs.get('newsletter_id')
        newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
        data['newsletter'] = newsletter
        return data


def start_sending(request, newsletter_id):
    """
    Запуск рассылки
    """
    newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
    if newsletter.status == 'created' and newsletter.date_time < datetime.now(ZONE):
        return redirect(reverse('newsletters:datetime_late', args=[newsletter_id]))
    newsletter.status = 'active'
    newsletter.save()
    return redirect(reverse('newsletters:newsletter_detail', args=[newsletter_id]))


def stop_sending(request, newsletter_id):
    """
    Остановка рассылки
    """
    newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
    newsletter.status = 'closed'
    newsletter.save()
    return redirect(reverse('newsletters:newsletter_detail', args=[newsletter_id]))

class DatetimeLateTemplateView(TemplateView):
    """
    Предупреждение о том что дата первой отправки рассылки - просрочена
    """
    template_name = 'newsletters/datetime_late.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['newsletter_id'] = self.kwargs.get('newsletter_id')
        return data

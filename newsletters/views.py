from itertools import product

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, TemplateView

from blog.models import Blog
from newsletters.forms import NewsletterForm, MessageForm, ClientForm
from newsletters.models import Newsletter, Message, Client, NewsletterReport
from newsletters.services import send_newsletter
from users.models import User


class CheckSimpleUser(UserPassesTestMixin):
    """
    Миксин проверяет: не является ли пользователь менеджером или суперпользователем
    """
    def test_func(self):
        return not self.request.user.is_superuser and not self.request.user.groups.filter(name='manager').exists()


class CheckManager(UserPassesTestMixin):
    """
    Миксин проверяет: является ли пользователь менеджером
    """
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists()

class CheckOwnerNewsletter(PermissionRequiredMixin):
    """
    Миксин проверяет что текущий пользователь является владельцем рассылки
    Или у пользователя есть права просматривать чужие рассылки
    """
    permission_required = 'newsletters.view_owner_newsletter'

    def has_permission(self):
        newsletter = get_object_or_404(Newsletter, pk=self.kwargs.get('pk'))
        return super().has_permission() or newsletter.user == self.request.user


class ManagerUserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'newsletters/manager_user_list.html'

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

class HomeListView(CheckSimpleUser, TemplateView):
    """
    Главная страница
    """
    model = Newsletter
    template_name = 'newsletters/home.html'

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
        else:
            data = Newsletter.objects.filter(user=user).order_by('-created_at')
        return data


class NewsletterDetailView(CheckOwnerNewsletter, DetailView):
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


class NewsletterCreateView(CreateView):
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


class NewsletterUpdateView(UpdateView):
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


class NewsletterDeleteView(DeleteView):
    model = Newsletter


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            data = Message.objects.all().order_by('title')
        else:
            data = Message.objects.filter(user=user).order_by('title')
        return data


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
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


class MessageUpdateView(UpdateView):
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


class MessageDeleteView(DeleteView):
    model = Message


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 30

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='manager').exists():
            data = Client.objects.all().order_by('-created_at')
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


class ClientCreateView(LoginRequiredMixin, CreateView):
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


class ClientUpdateView(LoginRequiredMixin, UpdateView):
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


class NewsletterReportListView(LoginRequiredMixin, ListView):
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
    newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
    if newsletter.status == 'closed':
        send_newsletter(newsletter)
    newsletter.status = 'active'
    newsletter.save()
    return redirect(reverse('newsletters:newsletter_detail', args=[newsletter_id]))


def stop_sending(request, newsletter_id):
    newsletter = get_object_or_404(Newsletter, pk=newsletter_id)
    newsletter.status = 'closed'
    newsletter.save()
    NewsletterReport.objects.create(
        newsletter=newsletter,
        is_success=False,
        report='Рассылка остановлена'
    )
    return redirect(reverse('newsletters:newsletter_detail', args=[newsletter_id]))

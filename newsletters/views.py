from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from newsletters.forms import NewsletterForm, MessageForm, ClientForm
from newsletters.models import Newsletter, Message, Client


class NewsletterListView(LoginRequiredMixin, ListView):
    """
    Отображение списка рассылок
    """
    model = Newsletter
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        data = Newsletter.objects.filter(user=user).order_by('-created_at')
        return data

class NewsletterDetailView(LoginRequiredMixin, DetailView):
    """
    Отображение информации о рассылке
    """
    model = Newsletter
    context_object_name = 'newsletter'


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
        data = Client.objects.filter(user=user).order_by('-created_at')
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

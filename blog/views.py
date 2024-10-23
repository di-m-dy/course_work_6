from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from blog.forms import BlogForm
from blog.models import Blog
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView



class BlogListView(LoginRequiredMixin, ListView):
    """
    Отображение списка постов
    """
    model = Blog
    paginate_by = 10

    def get_queryset(self):
        # сортировка по дате создания
        data = super().get_queryset().order_by('-created_at')
        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data()
        # обработка параметра - показывать неопубликованные
        hidden = self.request.GET.get('hidden')
        if hidden:
            data['hidden'] = True
        return data


class BlogDetailView(LoginRequiredMixin, DetailView):
    """
    Отображение поста
    """
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1 # счетчик просмотров
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    """
    Создание поста
    """
    model = Blog
    success_url = reverse_lazy('blog:blog')
    form_class = BlogForm



class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование поста
    """
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        return reverse('blog:post', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление поста
    """
    model = Blog
    success_url = reverse_lazy('blog:blog')

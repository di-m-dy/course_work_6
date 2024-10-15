from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from pytils.templatetags.pytils_translit import slugify
from blog.forms import BlogForm
from blog.models import Blog
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


# Create your views here.


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    paginate_by = 2

    def get_queryset(self):
        data = super().get_queryset().order_by('-created_at')
        return data

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data()
        hidden = self.request.GET.get('hidden')
        if hidden:
            data['hidden'] = True
        return data


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    success_url = reverse_lazy('blog:index')
    form_class = BlogForm

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    success_url = reverse_lazy('blog:index')
    form_class = BlogForm

    def get_success_url(self):
        return reverse('blog:post', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:index')


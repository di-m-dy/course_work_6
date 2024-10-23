from django.urls import path
from blog.views import BlogListView, BlogDetailView, BlogDeleteView, BlogCreateView, BlogUpdateView
from blog.services import set_cache_controller

app_name = 'blog'

urlpatterns = [
    path('', set_cache_controller(BlogListView.as_view()), name='blog'),
    path('post/<int:pk>', BlogDetailView.as_view(), name='post'),
    path('post/<int:pk>/delete', BlogDeleteView.as_view(), name='delete_post'),
    path('create', BlogCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/update', BlogUpdateView.as_view(), name='update_post')
]

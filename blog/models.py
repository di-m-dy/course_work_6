from django.db import models


# Create your models here.

class Blog(models.Model):
    """
    Модель блоговой записи
    """
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Cодержимое')
    image = models.ImageField(upload_to='blog_image', verbose_name='Превью')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    is_active = models.BooleanField(verbose_name='Признак публикации', default=True)
    views_count = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'пост для блога'
        verbose_name_plural = 'посты для блога'

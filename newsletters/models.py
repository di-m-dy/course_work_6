from django.db import models
from users.models import User


class Client(models.Model):
    """
    Информация о клиенте, которому будет реализована рассылка
    """
    user = models.ForeignKey(User, verbose_name='Пользователь рассылок', on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, verbose_name='Email клиента', unique=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя клиента')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия клиента')
    parent_name = models.CharField(max_length=255, verbose_name='Отчество клиента', null=True, blank=True)
    comment = models.CharField(max_length=255, verbose_name='Комментарий', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата добавления клиента')

    def __str__(self):
        parent_name = f" {self.parent_name}" if self.parent_name else ''
        return f"{self.first_name} {self.last_name}{parent_name}: {self.email}"

    class Meta:
        verbose_name = 'клиент для рассылки'
        verbose_name_plural = 'клиенты для рассылки'


class Message(models.Model):
    """
    Сообщение для рассылки
    """
    user = models.ForeignKey(User, verbose_name='Пользователь рассылок', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Заголовок сообщения')
    text = models.TextField(verbose_name='Текст сообщения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение для рассылки'
        verbose_name_plural = 'сообщения для рассылки'


class Newsletter(models.Model):
    """
    Настройки рассылки
        Cтатус:
            - created: рассылка создана но не запущена (при создании по-умолчанию)
            - active: рассылка запущена
            - closed: рассылка остановлена (автоматически после единоразовой рассылки или остановлена в ручную в регулярном режиме)
        Периодичность:
            - once: рассылается один раз
            - days: каждый день в одно и то же время
            - weeks: каждую неделю в то же время
            - weeks: Раз в 30 дней в одно и то же время
    """
    STATUS_CHOICES = [
        ('created', 'Рассылка создана'),
        ('active', 'Рассылка запущена'),
        ('closed', 'Рассылка завершена')
    ]
    PERIOD_CHOICES = [
        ('once', 'Единоразовая рассылка'),
        ('days', 'Ежедневная рассылка'),
        ('weeks', 'Еженедельная рассылка'),
        ('months', 'Ежемесячная рассылка'),
    ]
    user = models.ForeignKey(User, verbose_name='Пользователь рассылок', on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name='clients', verbose_name='Клиент для рассылки')
    message = models.ForeignKey(Message, verbose_name='Сообщение для рассылки', on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name='Дата и время отправки первой рассылки')
    period =  models.CharField(verbose_name='Периодичность рассылки', choices=PERIOD_CHOICES)
    status = models.CharField(verbose_name='Статус рассылки', choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания рассылки')

    def __str__(self):
        return f"Рассылка #{self.pk}: {self.date_time} ({self.created_at})"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = [
            ('view_owner_newsletter', 'Can view others owner newsletters'),
            ('set_closed_newsletter', 'Can set closed newsletters'),
        ]


class NewsletterReport(models.Model):
    """
    Информация о попытках рассылки
    """
    newsletter = models.ForeignKey(Newsletter, verbose_name='Рассылка', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True, verbose_name='Дата и время попытки рассылки')
    is_success = models.BooleanField(verbose_name='Попытка успешная')
    report = models.CharField(max_length=255, verbose_name='Отчет в случае ошибки попытки', null=True, blank=True)
    next_send = models.DateTimeField(
        verbose_name='Дата и время следующей попытки рассылки',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Попытка #{self.pk}: {self.date_time} (рассылка # {self.newsletter.pk}"

    class Meta:
        verbose_name = "попытка рассылки"
        verbose_name_plural = "попытки рассылки"

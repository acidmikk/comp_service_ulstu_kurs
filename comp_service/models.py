from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
from django.utils.text import slugify


def upload_to(instance, filename):
    return f'checks/{instance.user.username}/{filename}'


class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(verbose_name='Фото',
                              upload_to='gallery/%Y/%m/%d/',
                              null=False,
                              blank=False
                              )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='photos',
                               )
    published = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        verbose_name_plural = 'Фото'
        verbose_name = 'Фото'
        ordering = ('-published',)


class Service(models.Model):                                                # Услуга
    title = models.CharField(max_length=100)                                # Название услуги
    description = models.TextField()                                        # Описание
    cost = models.IntegerField(null=False, blank=False)                     # Стоимость
    published = models.DateTimeField(default=timezone.now, db_index=True)   # Дата добавления
    slug = models.SlugField(max_length=250)                                 # Ссылка услуги

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:service', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'Услуги'
        verbose_name = 'Услуга'
        ordering = ('-published',)


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('created', 'Создан'),
        ('in_progress', 'В работе'),
        ('ready', 'Готов'),
        ('completed', 'Выполнен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)                                    # Пользователь, который оставил заказ
    services = models.ManyToManyField(Service)                                                  # Услуги, входящие в заказ
    order_date = models.DateTimeField(auto_now_add=True)                                        # Дата заказа
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='created')   # Статус заказа
    check_file = models.FileField(upload_to=upload_to, null=True, blank=True)                   # Поле для чека
    slug = models.SlugField(max_length=250, unique=True)

    def get_absolute_url(self):
        return reverse('main:order', kwargs={'slug': self.slug})

    def total_cost(self):
        return sum(service.cost for service in self.services.all())

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username} on {self.order_date}"

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'
        ordering = ('-order_date',)

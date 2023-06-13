from django.db import models

# Create your models here.
from django.urls import reverse


class Plc(models.Model):
    class Meta:
        verbose_name = 'PLC'
        verbose_name_plural = 'PLC'
        ordering = ['id']

    name = models.CharField(max_length=255, verbose_name='Название')
    slag = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Ссылка')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', verbose_name='Фото')
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    room = models.ForeignKey('Room', on_delete=models.PROTECT, null=True, verbose_name='Электропомещение')

    def __str__(self):
        return f'{self.name}: {self.description}'

    def get_absolute_url(self):
        return reverse('plc', kwargs={'plc_slug': self.slag})


class Room(models.Model):
    class Meta:
        verbose_name = 'Электропомещение'
        verbose_name_plural = 'Электропомещения'

    name = models.CharField(max_length=255, db_index=True)
    slag = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('room', kwargs={'room_slug': self.slag})



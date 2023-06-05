from django.db import models

# Create your models here.
from django.urls import reverse


class Plc(models.Model):
    name = models.CharField(max_length=255)
    slag = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    room = models.ForeignKey('Room', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return f'{self.name}: {self.description}'

    def get_absolute_url(self):
        return reverse('plc', kwargs={'plc_slug': self.slag})


class Room(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slag = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'



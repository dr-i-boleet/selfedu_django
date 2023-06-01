from django.db import models

# Create your models here.
from django.urls import reverse


class Plc(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/')
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}: {self.description}'

    def get_absolute_url(self):
        return reverse('plc', kwargs={'plc_id': self.pk})



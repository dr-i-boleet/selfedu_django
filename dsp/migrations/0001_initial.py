# Generated by Django 4.2.1 on 2023-05-31 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('photo', models.ImageField(upload_to='photo/%Y/%m/%d/')),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_updated', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
            ],
        ),
    ]
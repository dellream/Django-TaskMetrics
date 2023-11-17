# Generated by Django 4.2.6 on 2023-11-16 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentary',
            name='email',
        ),
        migrations.RemoveField(
            model_name='commentary',
            name='name',
        ),
        migrations.AddField(
            model_name='commentary',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commentary',
            name='body',
            field=models.TextField(verbose_name='Комментарий'),
        ),
    ]
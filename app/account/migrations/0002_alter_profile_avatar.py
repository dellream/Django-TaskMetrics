# Generated by Django 4.2.6 on 2023-11-21 06:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='img/profile_avatars/default_profile_avatar.png', upload_to='img/profile_avatars/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], verbose_name='Фотография профиля'),
        ),
    ]
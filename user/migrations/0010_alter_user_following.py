# Generated by Django 4.1.3 on 2022-12-01 18:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_user_followers_user_blocked_user_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]

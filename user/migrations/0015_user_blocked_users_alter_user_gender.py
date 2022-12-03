# Generated by Django 4.1.3 on 2022-12-02 20:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_rename_bus_location_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='blocked_users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], default='Other', max_length=10),
        ),
    ]
# Generated by Django 4.1.3 on 2022-12-02 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_user_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_blocked',
        ),
    ]
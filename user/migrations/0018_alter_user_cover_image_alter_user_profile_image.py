# Generated by Django 4.1.3 on 2022-12-23 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_alter_user_blocked_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cover_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]

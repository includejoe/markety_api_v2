# Generated by Django 4.1.3 on 2023-02-11 22:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0003_comment_is_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='og_comment_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.expressions.Case, to=settings.AUTH_USER_MODEL),
        ),
    ]
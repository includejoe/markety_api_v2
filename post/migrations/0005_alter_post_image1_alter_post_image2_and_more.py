# Generated by Django 4.1.3 on 2023-02-05 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_image1_alter_post_image2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image1',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='image2',
            field=models.URLField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='image3',
            field=models.URLField(),
        ),
    ]

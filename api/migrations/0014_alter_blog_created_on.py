# Generated by Django 3.2.6 on 2021-08-19 15:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_blog_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

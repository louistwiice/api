# Generated by Django 3.2.6 on 2021-08-18 13:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_coachrating_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachrating',
            name='rating_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='fitnessprogramsrating',
            name='rating_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

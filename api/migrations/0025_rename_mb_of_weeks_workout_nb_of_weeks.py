# Generated by Django 3.2.6 on 2021-08-19 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_rename_name_workout_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workout',
            old_name='mb_of_weeks',
            new_name='nb_of_weeks',
        ),
    ]

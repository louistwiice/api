# Generated by Django 3.2.6 on 2021-08-19 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_fitnessprogramscomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='startdate',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

# Generated by Django 3.2.6 on 2021-08-17 16:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_usersfitnessprograms_joined_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitnessprogram',
            name='duree',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(30)], verbose_name='Number of time, in minute, for this Program'),
        ),
        migrations.AlterField(
            model_name='fitnessprogram',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]

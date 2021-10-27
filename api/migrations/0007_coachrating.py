# Generated by Django 3.2.6 on 2021-08-18 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_account_lastname'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoachRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Coach', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
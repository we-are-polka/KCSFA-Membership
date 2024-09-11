# Generated by Django 5.0.6 on 2024-09-11 21:45

import c_webapp.models
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('c_webapp', '0006_event_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=c_webapp.models.default_end_time),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]

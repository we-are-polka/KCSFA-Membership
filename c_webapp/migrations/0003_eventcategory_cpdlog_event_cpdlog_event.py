# Generated by Django 5.0.6 on 2024-09-10 16:15

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('c_webapp', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('points_per_event', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CPDLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points_earned', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c_webapp.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('attendees', models.ManyToManyField(through='c_webapp.CPDLog', to='c_webapp.profile')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c_webapp.eventcategory')),
            ],
        ),
        migrations.AddField(
            model_name='cpdlog',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='c_webapp.event'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-07 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('c_webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default-profile.jpg', upload_to='profile_pics/'),
        ),
    ]

# Generated by Django 2.1.15 on 2020-08-29 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0003_auto_20200823_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='is_occupied',
            field=models.BooleanField(default=False),
        ),
    ]

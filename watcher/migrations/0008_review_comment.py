# Generated by Django 3.1 on 2020-12-05 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0007_auto_20201205_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]

# Generated by Django 3.1 on 2020-12-08 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0011_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='watcher.store'),
        ),
    ]

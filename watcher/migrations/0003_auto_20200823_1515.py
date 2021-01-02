# Generated by Django 2.1.15 on 2020-08-23 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0002_auto_20200819_1642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('floor_num', models.IntegerField(default=-1)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='watcher.Store')),
            ],
        ),
        migrations.AddField(
            model_name='camera',
            name='floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='watcher.Floor'),
        ),
        migrations.AddField(
            model_name='table',
            name='floor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='watcher.Floor'),
        ),
    ]
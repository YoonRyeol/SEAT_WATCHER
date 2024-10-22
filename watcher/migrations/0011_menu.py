# Generated by Django 3.1 on 2020-12-08 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0010_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('price', models.CharField(blank=True, max_length=128, null=True)),
                ('category_name', models.CharField(blank=True, max_length=128, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='watcher.category')),
            ],
        ),
    ]

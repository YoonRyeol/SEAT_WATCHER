# Generated by Django 3.1 on 2020-12-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0008_review_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='review_score',
            field=models.DecimalField(decimal_places=2, max_digits=3),
        ),
    ]

# Generated by Django 2.2 on 2020-07-08 02:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 8, 2, 9, 21, 374184, tzinfo=utc)),
        ),
    ]
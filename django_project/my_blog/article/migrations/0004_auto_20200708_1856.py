# Generated by Django 2.2 on 2020-07-08 10:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200708_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 8, 10, 56, 14, 585112, tzinfo=utc)),
        ),
    ]
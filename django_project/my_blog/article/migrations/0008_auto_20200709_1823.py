# Generated by Django 2.2 on 2020-07-09 10:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20200709_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecolumn',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 9, 10, 23, 45, 172407, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 9, 10, 23, 45, 173406, tzinfo=utc)),
        ),
    ]
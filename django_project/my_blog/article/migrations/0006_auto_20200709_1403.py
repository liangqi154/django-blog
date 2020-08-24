# Generated by Django 2.2 on 2020-07-09 06:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('article', '0005_auto_20200709_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='articlecolumn',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 9, 6, 3, 22, 44984, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 9, 6, 3, 22, 44984, tzinfo=utc)),
        ),
    ]

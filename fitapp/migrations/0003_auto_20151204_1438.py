# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0002_initial_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeseriesdata',
            options={'get_latest_by': 'date'},
        ),
        migrations.AddField(
            model_name='timeseriesdata',
            name='intraday',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='timeseriesdata',
            name='date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='timeseriesdata',
            unique_together=set([('user', 'resource_type', 'date', 'intraday')]),
        ),
        migrations.AddField(
            model_name='timeseriesdatatype',
            name='intraday_support',
            field=models.BooleanField(default=False),
            preserve_default=True
        )
    ]

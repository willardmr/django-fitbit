# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_intraday_support(apps, schema_editor):
    """
    Marks TimeSeriesDataType instances that support intraday data as per Fitbit
    documentation.
    """
    resources = ['calories', 'steps', 'distance', 'floors', 'elevation']

    TimeSeriesDataType = apps.get_model("fitapp", "TimeSeriesDataType")
    supported = TimeSeriesDataType.objects.filter(category=1,
                                                  resource__in=resources)
    supported.update(intraday_support=True)


def remove_intraday_support(apps, schema_editor):
    """
    Since the intraday_support field will be removed upon migrating backwards,
    do nothing.
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('fitapp', '0003_auto_20151204_1438'),
    ]

    operations = [
        migrations.RunPython(add_intraday_support, remove_intraday_support)
    ]

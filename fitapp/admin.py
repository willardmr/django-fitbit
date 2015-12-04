from django.contrib import admin

from . import models


admin.site.register(models.UserFitbit)
admin.site.register(models.TimeSeriesData)
admin.site.register(models.TimeSeriesDataType)

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


UserModel = getattr(settings, 'FITAPP_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class UserFitbit(models.Model):
    user = models.OneToOneField(UserModel)
    fitbit_user = models.CharField(max_length=32, unique=True)
    auth_token = models.TextField()
    auth_secret = models.TextField()

    def __str__(self):
        return self.user.__str__()

    def get_user_data(self):
        return {
            'resource_owner_key': self.auth_token,
            'resource_owner_secret': self.auth_secret,
            'user_id': self.fitbit_user,
        }


class TimeSeriesDataType(models.Model):
    """
    This model is intended to store information about Fitbit's time series
    resources, which can be found here:
    https://wiki.fitbit.com/display/API/API-Get-Time-Series
    """

    foods = 0
    activities = 1
    sleep = 2
    body = 3
    CATEGORY_CHOICES = (
        (foods, 'foods'),
        (activities, 'activities'),
        (sleep, 'sleep'),
        (body, 'body'),
    )
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    resource = models.CharField(max_length=128)
    intraday_support = models.BooleanField(default=False)

    def __str__(self):
        return self.path()

    class Meta:
        unique_together = ('category', 'resource',)
        ordering = ['category', 'resource']

    def path(self):
        return '/'.join([self.get_category_display(), self.resource])


class TimeSeriesData(models.Model):
    """
    The purpose of this model is to store Fitbit user data obtained from their
    time series API (https://wiki.fitbit.com/display/API/API-Get-Time-Series).

    Intraday data only: user's timezone is retrieved and used to convert data to
    UTC prior to saving.
    """

    user = models.ForeignKey(UserModel)
    resource_type = models.ForeignKey(TimeSeriesDataType)
    date = models.DateTimeField()
    value = models.CharField(null=True, default=None, max_length=32)
    intraday = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'resource_type', 'date', 'intraday')
        get_latest_by = 'date'

    def string_date(self):
        return self.date.strftime('%Y-%m-%d')

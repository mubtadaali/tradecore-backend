from django.conf import settings
from django.db import models


class Profile(models.Model):
    city = models.CharField(max_length=48, null=True, blank=True)
    region = models.CharField(max_length=48, null=True, blank=True)
    postal_code = models.CharField(max_length=5, null=True, blank=True)
    country_code = models.CharField(max_length=2, null=True, blank=True)
    timezone = models.CharField(max_length=32, null=True, blank=True)
    currency_code = models.CharField(max_length=8, null=True, blank=True)
    joined_day_holiday = models.CharField(
        max_length=32, null=True, blank=True, verbose_name='Name of the holiday on user\'s joined day'
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE, primary_key=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

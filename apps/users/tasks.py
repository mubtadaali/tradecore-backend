from celery.exceptions import Retry
from django.contrib.auth.models import User
from requests import ConnectTimeout

from apps.users.models import Profile
from tradecore.celery import app

from apps.services.abstractapi import retrieve_geo_location_data, retrieve_holiday_information


@app.task(bind=True)
def add_user_geolocation_data(self, ip_address, username):
    """
    enrich user profile with geolocation data
    :param ip_address: (str) request user's ip address
    :param username: (str) created user's username
    """
    try:
        response = retrieve_geo_location_data(ip_address)
        if response.status_code != 200:
            self.retry(countdown=2, max_retries=3)

        response = response.json()
        timezone = response.pop('timezone', {}).get('name')
        currency_code = response.pop('currency', {}).get('currency_code')
        response.update({'timezone': timezone, 'currency_code': currency_code})

        Profile.objects.filter(user__username=username).update(**response)
        retrieve_holiday_info.delay(currency_code, username)
    except Retry:
        pass
    except ConnectTimeout:
        self.retry(countdown=2, max_retries=3)


@app.task(bind=True)
def retrieve_holiday_info(self, country_code, username):
    """
    enrich user profile with geolocation data
    :param country_code: (str) user's country code
    :param username: (str) created user's username
    """
    user = User.objects.get(username=username)
    joined_date = user.date_joined
    try:
        req_params = {
            'country': country_code, 'year': joined_date.year,
            'month': joined_date.month, 'day': joined_date.day
        }
        response = retrieve_holiday_information(req_params)
        if response.status_code != 200:
            self.retry(countdown=2, max_retries=3)

        if response.json():
            holiday_name = response.json()[0].get('name')
            Profile.objects.filter(pk=user.id).update(joined_day_holiday=holiday_name)
    except Retry:
        pass
    except ConnectTimeout:
        self.retry(countdown=2, max_retries=3)

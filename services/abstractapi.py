import requests
from django.conf import settings

from services.exceptions import EmailValidationTimeoutException
from services.utils import requests_retry_session

BASE_URL_T = 'https://{}.abstractapi.com/v1'


def is_email_deliverable(email):
    params = {'email': email, 'api_key': settings.ABSTRACT_EMAIL_VALIDATION_API_KEY}
    request = requests_retry_session()
    try:
        response = request.get(url=BASE_URL_T.format('emailvalidation'), params=params)
        return 'DELIVERABLE' == response.json().get('deliverability').upper()
    except Exception:
        raise EmailValidationTimeoutException


def retrieve_geo_location_data(ip_address):
    params = {
        'api_key': settings.ABSTRACT_GEOLOCATION_API_KEY,
        'fields': 'city,country_code,region,postal_code,timezone,currency',
        'ip_address': ip_address,
    }
    return requests.get(url=BASE_URL_T.format('ipgeolocation'), params=params, timeout=10)


def retrieve_holiday_information(params):
    params.update({'api_key': settings.ABSTRACT_HOLIDAYS_API_KEY})
    return requests.get(url=BASE_URL_T.format('holidays'), params=params, timeout=10)

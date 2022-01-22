from django.conf import settings

from apps.services.exceptions import EmailValidationTimeoutException
from apps.services.utils import requests_retry_session

BASE_URL_T = 'https://{}.abstractapi.com/v1'


def is_email_deliverable(email):
    params = {'email': email, 'api_key': settings.ABSTRACT_API_KEY}
    request = requests_retry_session()
    try:
        response = request.get(url=BASE_URL_T.format('emailvalidation'), params=params)
        return 'DELIVERABLE' == response.json().get('deliverability').upper()
    except Exception:
        raise EmailValidationTimeoutException

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tradecore',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
ALLOWED_HOSTS = []
DEBUG = True  # Only for local env
ABSTRACT_EMAIL_VALIDATION_API_KEY = ''  # Add your key here
ABSTRACT_GEOLOCATION_API_KEY = ''  # Add your key here
ABSTRACT_HOLIDAYS_API_KEY = ''  # Add your key here

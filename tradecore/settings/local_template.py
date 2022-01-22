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
ABSTRACT_API_KEY = ''  # Add your key here

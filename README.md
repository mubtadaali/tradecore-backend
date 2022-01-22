# TradeCore - Backend
### Overview

A social application where people can share their thoughts via posts and other people can share their response on 
that by liking and unliking the post.


### Basic Requirements
  * Python 3.10.0
  * PostgreSQL 14.1

### Installing

Clone the project

```
git clone git@github.com:mubtadaali/tradecore-backend.git
```
Create & activate an environment for this project with Python 3.10
```
virtualenv environment_name 
```
Install all the required libraries for this project
```
pip3 install -r requirements.txt
```
Create `local.py` file in unlisted/settings
```
DEBUG = True
ALLOWED_HOSTS = [*]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '[ADD_DATABASE_NAME_HERE]',
        'USER': '[ADD_USER_HERE]',
        'PASSWORD': '[ADD_PASSWORD_HERE]',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```
Apply the migrations 
```
python manage.py migrate
```
Create a super user
```
python manage.py createsuperuser
```
Run the python server
```
python manage.py runserver
```

"""
Django settings for ExskilenceTest project.

Generated by 'django-admin startproject' using Django 4.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hn&0l#@s16(1#6ea-0ii$z1f51+1ro!akv)sx#_5-%wv97kcj7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework', 
    'djongo',
    'Aptitest',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://exskilence-internships.azurewebsites.net/',
    'https://internships.exskilence.com/',
    'https://thoughtprocesstest.azurewebsites.net',
]

CSRF_TRUSTED_ORIGINS=[ 
    'https://exskilence-internships.azurewebsites.net/',
    'https://internships.exskilence.com/',
    'https://thoughtprocesstest.azurewebsites.net',
]
ROOT_URLCONF = 'ExskilenceTest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ExskilenceTest.wsgi.application'

AZURE_ACCOUNT_NAME = 'storeholder'
AZURE_ACCOUNT_KEY = 'QxlUJdp8eSoPeQPas4NigSkXg6KMep7z+fPQ5CpPm0kRfjg7Q0lFmVEIyhU4ohFLFdSqntDAG6MY84elTfecnw=='
AZURE_CONTAINER = 'tpdata'

MSSQL_SERVER_NAME = 'slnkshmtbsil.database.windows.net'
MSSQL_DATABASE_NAME = 'exe_test'
MSSQL_USERNAME = 'tpssa'
MSSQL_PWD = 'TPSuser@sa123'
MSSQL_DRIVER =  'ODBC Driver 17 for SQL Server'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

from urllib.parse import quote_plus
uname = 'EUAdmin'
pwd = 'EUServer@sa123'
escaped_username = quote_plus(uname)
escaped_password = quote_plus(pwd)
uri = f"mongodb+srv://{escaped_username}:{escaped_password}@eucluster.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'ExskilenceDb',
        'ENFORCE_SCHEMA': False,  
        'CLIENT': {
            'host': uri,
            'username': uname,
            'password': pwd,
            'authMechanism': 'SCRAM-SHA-256',
        }
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'ExskilenceAPT',
#         'ENFORCE_SCHEMA': False,  
#         'CLIENT': {
#             'host': 'mongodb+srv://kecoview:FVy5fqqCtQy3KIt6@cluster0.b9wmlid.mongodb.net/',
#             'username': 'kecoview',
#             'password': 'FVy5fqqCtQy3KIt6',
#             'authMechanism': 'SCRAM-SHA-1',
#         }
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

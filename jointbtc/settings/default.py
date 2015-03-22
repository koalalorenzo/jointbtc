# -*- coding: utf-8 -*-
"""
Django settings for jointbtc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
DEFAULT_SECRET_KEY = '+fddo$$@8vmkpwz*-b00h7_7+4pmikbc0o9os$*25cdly9h6!a'
SECRET_KEY = os.environ.get('SECRET_KEY', DEFAULT_SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payments',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'jointbtc.urls'

WSGI_APPLICATION = 'jointbtc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Parse database configuration from $DATABASE_URL
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Blockchain data
BLOCKCHAIN_API_CODE = os.environ.get('BLOCKCHAIN_API_CODE', "True")
GENERATE_WALLET = os.environ.get('GENERATE_WALLET', "True")

if GENERATE_WALLET == "True":
    from blockchain import createwallet
    import random
    import string

    WALLET_PASSWORD = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
    WALLET = createwallet.create_wallet(WALLET_PASSWORD, BLOCKCHAIN_API_CODE)
    WALLET_ID = WALLET.identifier
    print(WALLET_ID, WALLET_PASSWORD)

else:
    WALLET_ID = os.environ.get('WALLET_ID', "")
    WALLET_PASSWORD = os.environ.get('WALLET_PASSWORD', "")
    WALLET = None

# Fees Wallet Addresses

DEFAULT_TRANSACTION_FEE = int(0.0002 * 100000000)  # Satoshis
SERVICE_FEE_AMOUNT = int(0.0006 * 100000000)  # Satoshis
SERVICE_FEE_ADDRESS = "1GsAxo7aiuBkTAoUgb4ePWhUrBm9YW9cTq"
DEFAULT_TRANSACTION_NOTE = "testing"

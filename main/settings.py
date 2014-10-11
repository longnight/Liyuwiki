#coding=utf-8
"""
Django settings for main project.

"""
import private_settings
import djcelery
djcelery.setup_loader()

BROKER_URL = private_settings.BROKER_URL

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = private_settings.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = private_settings.DEBUG

TEMPLATE_DEBUG = private_settings.TEMPLATE_DEBUG

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

ALLOWED_HOSTS = private_settings.ALLOWED_HOSTS

CSRF_COOKIE_DOMAIN = private_settings.CSRF_COOKIE_DOMAIN

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'secretballot',
    'south',
    'djcelery',
    'wikidict',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'secretballot.middleware.SecretBallotIpUseragentMiddleware',
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'main.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': private_settings.local_db_name,
        'USER': private_settings.local_db_user,
        'PASSWORD': private_settings.local_db_pwd,
        'HOST': '',
        'PORT': '',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'ENGINE': 'wikidict.whoosh_cn_backend.WhooshEngine',
        # 'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh_CN'
# LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Chongqing'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = ''

STATIC_PATH = os.path.join(PROJECT_PATH, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

ADMINS = private_settings.admin_mail

EMAIL_BACKEND = private_settings.EMAIL_BACKEND
EMAIL_HOST = private_settings.EMAIL_BACKEND
EMAIL_HOST_USER = private_settings.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = private_settings.EMAIL_HOST_PASSWORD
EMAIL_PORT = private_settings.EMAIL_PORT

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'liyuwikicache01',
        'TIMEOUT': 60 * 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    },
    'cache2': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'liyuwikicache02',
        'TIMEOUT': 60 * 60 * 24 * 90,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
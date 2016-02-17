"""
Django settings for mrfantastic project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import dj_database_url
from decouple import Csv, config

import raven


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.join(BASE_DIR, '..'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

AUTHENTICATION_BACKENDS = (
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Application definition

INSTALLED_APPS = [
    # Project specific apps
    'mrfantastic.base',
    'mrfantastic.simplex',
    # Third party apps
    'django_jinja',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #Raven logging
    'raven.contrib.django.raven_compat',
    # The Django sites framework is required
    'django.contrib.sites',
    #Social authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bungiesearch',
]
BUNGIESEARCH = {
    'URLS': ['0.0.0.0'], # No leading http:// or the elasticsearch client will complain.
    'INDICES': {'main_index': 'mrfantastic.simplex.modelindex'}, # Must be a module path.
    'SIGNALS': {'BUFFER_SIZE': 1},
    'TIMEOUT': 5
}
SITE_ID = 1
RAVEN_CONFIG = {
    'dsn': config('DSN')
}
for app in config('EXTRA_APPS', default='', cast=Csv()):
    INSTALLED_APPS.append(app)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_csrf.CsrfMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
)

ROOT_URLCONF = 'mrfantastic.urls'

WSGI_APPLICATION = 'mrfantastic.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=dj_database_url.parse
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = config('USE_I18N', default=True, cast=bool)

USE_L10N = config('USE_L10N', default=True, cast=bool)

USE_TZ = config('USE_TZ', default=True, cast=bool)

STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'static'))
STATIC_URL = config('STATIC_URL', '/static/')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))
MEDIA_URL = config('MEDIA_URL', '/media/')


SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.jinja',
            'newstyle_gettext': True,
            'context_processors': [
                'session_csrf.context_processor',
                'mrfantastic.base.context_processors.settings',
                'mrfantastic.base.context_processors.i18n',
            ],
        }
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'session_csrf.context_processor',
                'django.template.context_processors.request',
            ],
        }
    },
]

TEMPLATE_DIRS = (
    # allauth templates: you could copy this directory into your
    # project and tweak it according to your needs
    # os.path.join(PROJECT_ROOT, 'templates', 'uniform', 'allauth'),
    # example project specific templates /mrfantastic/templates/allauth
    os.path.join(ROOT ,'mrfantastic', 'templates', 'allauth'),
)

# Django-CSP
CSP_DEFAULT_SRC = (
    "'self'",
)
CSP_FONT_SRC = (
    "'self'",
    'http://*.mozilla.net',
    'https://*.mozilla.net',
    'http://*.mozilla.org',
    'https://*.mozilla.org',
)
CSP_IMG_SRC = (
    "'self'",
    'http://*.mozilla.net',
    'https://*.mozilla.net',
    'http://*.mozilla.org',
    'https://*.mozilla.org',
)
CSP_SCRIPT_SRC = (
    "'self'",
    'http://*.mozilla.org',
    'https://*.mozilla.org',
    'http://*.mozilla.net',
    'https://*.mozilla.net',
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'http://*.mozilla.org',
    'https://*.mozilla.org',
    'http://*.mozilla.net',
    'https://*.mozilla.net',
)

# This is needed to get a CRSF token in /admin
ANON_ALWAYS = True

"""
Django settings for contentcuration project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STORAGE_ROOT = os.path.join(BASE_DIR, "storage")

STATIC_ROOT = os.path.join(BASE_DIR, "static")
DB_ROOT = os.path.join(BASE_DIR, "databases")

PERMISSION_TEMPLATE_ROOT = os.path.join(BASE_DIR, "contentcuration", "templates", "permissions")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_s0k@&o%m6bzg7s(0p(w6z5xbo%vy%mj+xx(w3mhs=f0ve0+h2' # TODO(aron): generate secret key, secretly!

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = ["*"]  # In production, we serve through a file socket, so this is OK.


# Application definition

INSTALLED_APPS = (
    'contentcuration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_js_reverse',
    'kolibri.content',
    'email_extras',
    'le_utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

#REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
 #   'DEFAULT_PERMISSION_CLASSES': [
 #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
  # ]
#}

ROOT_URLCONF = 'contentcuration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/templates/'],
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

WSGI_APPLICATION = 'contentcuration.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgres',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'contentcuration',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'learningequality',
        'PASSWORD': 'kolibri',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    },
    'export_staging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'export_staging.sqlite3')
    }
}


DATABASE_ROUTERS = [
    "contentcuration.router.Router"
]


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STORAGE_URL = '/storage/'

LOGIN_REDIRECT_URL = '/channels/'

AUTH_USER_MODEL = 'contentcuration.User'

ACCOUNT_ACTIVATION_DAYS=7
REGISTRATION_OPEN = True
SITE_ID = 1

# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 8000
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'Kolibri Content Curation <info@learningequality.org>'
DEFAULT_LICENSE = 1

SERVER_EMAIL = 'curation-errors@learningequality.org'
ADMINS = [('Errors', SERVER_EMAIL)]

IGNORABLE_404_URLS = [
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]

"""
Django settings for alfa project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-p6p1#*gkvn9wattj0ml3f$73+k$4#)dxgffcr%c)ly*bfm#6v_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','192.168.1.7','ALFA','alfa']

########################
# Application definition

INSTALLED_APPS = [
    'dte.apps.DteConfig',
    'manager.apps.ManagerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'wkhtmltopdf',
    'pdfkit',
    'num2words',
    'crispy_forms',
    'crispy_bootstrap4',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'alfa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'alfa/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dte.context_processors.user_empresa_context',
                'dte.context_processors.username_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'alfa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'marl0nH'), # jqiajkthdz
        'PASSWORD': os.environ.get('DB_PASSWORD', 'Ammh0909$'), # YGOR24H577XH22G2$
        'HOST': os.environ.get('DB_HOST', 'mirage.postgres.database.azure.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}  

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/El_Salvador'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PROJECT_DIR=os.path.dirname(__file__)
STATIC_ROOT= os.path.join(PROJECT_DIR,'staticfiles/')
STATIC_DIR= os.path.join(PROJECT_DIR,'static')
STATIC_URL = 'static/'
STATICFILES_DIRS = ( os.path.join(PROJECT_DIR,'static/'),)
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#WKHTMLTOPDF_CMD = '/path/to/my/wkhtmltopdf'
#WKHTMLTOPDF_CMD_OPTIONS = {
#    'page-size': 'Letter',
#    'page-height': '11in',
#    'page-width': '8.5in',
#    'margin-top': '0.5in',
#    'margin-right': '0.5in',
#    'margin-bottom': '0.5in',
#    'margin-left': '0.5in',
#    'encoding': 'UTF-8',
#    'no-outline': None
#}

#WKHTMLTOPDF_BIN = os.path.join(BASE_DIR, 'wkhtmltopdf')
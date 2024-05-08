import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
#STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
PROJECT_DIR=os.path.dirname(__file__)
STATIC_ROOT= os.path.join(PROJECT_DIR,'staticfiles/')
STATIC_DIR= os.path.join(PROJECT_DIR,'static')
STATIC_URL = 'static/'
STATICFILES_DIRS = ( os.path.join(PROJECT_DIR,'static/'),)
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media/')

#connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
#parameters = {pair.split('='):pair.split('=')[1] for pair in connection_string.split(' ')}

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		#'NAME': parameters['dbname'],
		#'HOST': parameters['host'],
		#'USER': parameters['user'],
		#'PASSWORD': parameters['password'],
		'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'marl0nH'), # jqiajkthdz
        'PASSWORD': os.environ.get('DB_PASSWORD', 'Ammh0909$'), # YGOR24H577XH22G2$
        'HOST': os.environ.get('DB_HOST', 'mirage.postgres.database.azure.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
	}
}



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
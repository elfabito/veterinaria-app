"""
Django settings for veterinaria project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import dj_database_url
from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib import messages
#from storages.backends.azure_storage import AzureStorage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env_path = Path('.', '.env')
load_dotenv(dotenv_path=env_path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
SITE_ID=1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mascotas',
    'django.contrib.sites',
    'xhtml2pdf',
    'corsheaders',
]
AUTH_USER_MODEL = 'mascotas.CustomUser'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

ROOT_URLCONF = 'veterinaria.urls'
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = os.getenv('CORS', '').split(',')

MESSAGE_TAGS = {
    messages.DEBUG: 'alert alert-dark',
    messages.INFO: 'alert alert-info',
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
}
USE_X_FORWARDED_HOST = True

SITE_ID=1
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'mascotas' / 'templates'],
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mascotas', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

WSGI_APPLICATION = 'veterinaria.wsgi.application'

#Stripe API KEYS
#STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")
#STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# #PayPal API KEYS
#PAYPAL_MODE = os.getenv("PAYPAL_MODE")
#PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
#PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")

# #Google Calendar API KEYS
#GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = 'credentials.json'
#GOOGLE_TOKEN_FILE = 'token.json'
#OAUTH2_CLIENT_ID = os.getenv('OAUTH2_CLIENT_ID')
#OAUTH2_CLIENT_SECRET = os.getenv('OAUTH2_CLIENT_SECRET')

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
#EMAIL_HOST_USER = str(os.getenv('USER_MAIL'))
#EMAIL_HOST_PASSWORD = str(os.getenv('USER_MAIL_PASSWORD'))
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'Patitas Contentas Team <noreply@patitascontentas.com>'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = BASE_DIR / "sent_emails"


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_TZ = True

USE_L10N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



MEDIA_ROOT = os.path.join(BASE_DIR,'media') 



# Configuraciones de Azure
# AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
# AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
# AZURE_CONTAINER = os.getenv('AZURE_CONTAINER')
# AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'

# Configuración de almacenamiento predeterminado
# DEFAULT_FILE_STORAGE = 'veterinaria.azure_storage.AzureMediaStorage'

# MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

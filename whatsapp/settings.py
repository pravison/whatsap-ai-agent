"""
Django settings for whatsapp project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import psycopg2
import environ
import os

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app', '127.0.0.1', '.salesflowpro.xyz']


# Application definition

SHARED_APPS = (
    'django_tenants',  # mandatory
    'clients', # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #packages 
    'tinymce',

)

TENANT_APPS = (
    # your tenant-specific apps
    #additional app
    'business',
    'customers',
    'ai',
    'accounts',
    'store',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #packages 
    'tinymce',
)

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]
TENANT_MODEL = "clients.Client"
TENANT_DOMAIN_MODEL ="clients.Domain"

LOGIN_URL = '/admin/login/'

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'whatsapp.urls'
PUBLIC_SCHEMA_URLCONF = 'whatsapp.urls_public'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'whatsapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


import dj_database_url 

DATABASES = {
    'default': dj_database_url.parse(
        env('POSTGRESQL'),
        conn_max_age=600,
        conn_health_checks=True,
        engine="django_tenants.postgresql_backend",
    )
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django_tenants.postgresql_backend",
#         "NAME": "tsdb",
#         "USER": "tsdbadmin",
#         "PASSWORD": env('PASSWORD'),
#         "HOST": env('HOST'),
#         "PORT": env('PORT'),
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
VERCEL_BLOB_URL = env('VERCEL_BLOB_URL')
MEDIA_URL = f'{VERCEL_BLOB_URL}media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WHATSAPP_URL =env('WHATSAPP_URL')
WHATSAPP_TOKEN =env('WHATSAPP_TOKEN')
OPENAI_API_KEY =env('OPENAI_KEY')

# KEEP session active for a year
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365 #365 DAYS

SESSION_EXPIRE_AT_BROWSER_CLOSE = False


SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
SECURE_PROXY_SSL_HEADER = ( 'HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

# # storage settings for vercel blob
# # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# # # vecel configurations 
# # AWS_ACCESS_KEY_ID = env('VERCEL_BLOB_ACCESS_KEY_ID')
# # AWS_SECRET_ACCESS_KEY = env('VERCEL_BLOB_SECRET_ACCESS_KEY')
# # AWS_STORAGE_BUCKET_NAME = 'my vercel blob bucket name'
# # AWS_S3_REGION_NAME = 'my vercel region name'
# # AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.blob.vercel-storage.com'
# # AWS_QUERYSTRING_AUTH = False # this makesfiles public without aunthentication

# STATIC_URL = f'htpps://{AWS_S3_CUSTOM_DOMAIN}/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# MEDIA_URL = f'htpps://{AWS_S3_CUSTOM_DOMAIN}/media/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
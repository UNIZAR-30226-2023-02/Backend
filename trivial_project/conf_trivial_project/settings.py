"""
Django settings for conf_trivial_project project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-fxjcca#eigq-w_x&k+z!39@nd5a8wn$8zo$f%cm%4i(d)o05cn"

SITE_NAME = 'Trivial'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

#Para hacer pruebas permitir todos los hosts
if not DEBUG:
   ALLOWED_HOSTS = ["*"]

# RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
# if RENDER_EXTERNAL_HOSTNAME:
#     ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

DJANGO_APPS = [
    "channels",
    'daphne',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "trivial_api",
    "sala",
    "partida",
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    "whitenoise.runserver_nostatic",
    'drf_spectacular',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

ASGI_APPLICATION = 'conf_trivial_project.asgi.application'

#Esto hay que cambiarlo en produccion(deployment)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = "conf_trivial_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'build')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "conf_trivial_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# For localhost
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
        "NAME": "trivial_bbdd",
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD":"",
        "PORT":"3306",
    }
}


if not DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            'OPTIONS': {
                'sql_mode': 'STRICT_TRANS_TABLES',
            },
            "NAME": "trivialdb",
            "HOST": "localhost",
            "USER": "api",
            "PASSWORD":"servidorPS2223",
            "PORT":"3306",
        }
    }


DATABASES["default"]["ATOMIC_REQUESTS"] = True

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3000',
#     'http://localhost:8000',
# ]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:8000',
]




# if not DEBUG:
#     CORS_ORIGIN_WHITELIST = [
#     'http://51.142.118.71:8000',
#     ]

#     CSRF_TRUSTED_ORIGINS = [
#     'http://51.142.118.71:8000',
#     ]

CORS_ORIGIN_ALLOW_ALL = True


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "trivial_api.Usuario"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # El orden en el que se muestra en la API Documentation
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'utils.exceptionhandler.custom_exception_handler'
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     # Para pedir que esten autenticados al acceder a la API
    #     'rest_framework.permissions.IsAuthenticated',
    #     'rest_framework.permissions.AllowAny',
    # ],
}

SPECTACULAR_SETTINGS = {
    # other settings
    'TITLE': 'Trivial API',
    'DESCRIPTION': 'This is the API for the Trivial project',
    'VERSION': '1.0.0',
    # Solo genera la documentacion de las url del trivial_api
    'SERVE_URLCONF': 'trivial_api.urls',
    'SERVE_INCLUDE_SCHEMA': False,
    'DISABLE_ERRORS_AND_WARNINGS': False,
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

FILE_UPLOAD_PERMISSIONS = 0o640

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)
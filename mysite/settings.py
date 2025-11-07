"""
Django settings for mysite project.
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# -------------------------------------------------------------------
# PATHS
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# MESSAGE TAGS
# -------------------------------------------------------------------
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Compatibility for python_2_unicode_compatible (your codebase requires it)
from six import python_2_unicode_compatible
import django.utils.encoding
django.utils.encoding.python_2_unicode_compatible = python_2_unicode_compatible


# -------------------------------------------------------------------
# KEYS + API
# -------------------------------------------------------------------
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")

SECRET_KEY = 'SECRET_KEY'
SECRET = os.getenv('payment')
STRIPE_KEY = 'SECRET'

DEBUG = True
ALLOWED_HOSTS = ['*']

# -------------------------------------------------------------------
# INSTALLED APPS
# -------------------------------------------------------------------
INSTALLED_APPS = [
    'admin_interface',
    'allauth',
    "allauth.socialaccount",
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'showcase',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

# -------------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

ROOT_URLCONF = 'mysite.urls'

INTERNAL_IPS = ['127.0.0.1']

# -------------------------------------------------------------------
# TEMPLATES
# -------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# -------------------------------------------------------------------
# DATABASE
# -------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
        },
    }
}

# -------------------------------------------------------------------
# AUTHENTICATION BACKENDS
# -------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    "django.contrib.auth.backends.ModelBackend",
    "showcase.backends.UpdatedUsernameBackend",
    "guest_user.backends.GuestBackend",
]

# -------------------------------------------------------------------
# PASSWORD VALIDATORS
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------------
# I18N / L10N / TIMEZONE
# -------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Europe/Paris'

# -------------------------------------------------------------------
# STATIC & MEDIA CONFIG (FIXED ✅)
# -------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------------------------------------------
# X-FRAME + LOGIN
# -------------------------------------------------------------------
X_FRAME_OPTIONS = '*'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# -------------------------------------------------------------------
# ENVIRONMENT VARS
# -------------------------------------------------------------------
import environ
env = environ.Env()
environ.Env.read_env()

# -------------------------------------------------------------------
# WARNINGS
# -------------------------------------------------------------------
import warnings
warnings.filterwarnings(
    'error',
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r'django\.db\.models\.fields',
)

# -------------------------------------------------------------------
# SOCIAL AUTH
# -------------------------------------------------------------------
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'

SOCIAL_AUTH_FACEBOOK_KEY = 'SOCIAL_AUTH_FACEBOOK_KEY'
SOCIAL_AUTH_FACEBOOK_SECRET = 'SOCIAL_AUTH_FACEBOOK_SECRET'


# -------------------------------------------------------------------
# CSRF SETTINGS
# -------------------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    'http://0.0.0.0:3000',
    'http://0.0.0.0:8000',
    'http://127.0.0.1:8000',
    'https://poketrove-official-website.onrender.com',
    'https://poketrove.org',
    'https://poketrove.net',
    'https://www.poketrove.store',
    'https://poketrove.store',
]

DATA_UPLOAD_MAX_NUMBER_FIELDS = 200000

DEFAULT_PAGINATE_BY = 10
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

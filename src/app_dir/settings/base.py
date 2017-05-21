"""
Django settings for app_dir project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from environ import Path
from app_dir.utils.environ import Env

ROOT_DIR = Path(__file__) - 3  # Three folders back

APPS_DIR = ROOT_DIR.path('app_dir')

# Nothing initially
env = Env(
)

# Read .env file
env_file = str(ROOT_DIR.path('.env'))
env.read_env(env_file)

SITE_ROOT = ROOT_DIR()

DEBUG = env.bool('DJANGO_DEBUG', False)

if DEBUG:
    # require it only for debug=False, let user ignore it for debug=True
    SECRET_KEY = env('DJANGO_SECRET_KEY', default='XXX')
else:
    SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = env(
    'DJANGO_ALLOWED_HOSTS',
    default='*'
).split(',')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

THIRD_PARTY_APPS = [
    'rest_framework_swagger',
    'rest_framework',
    'formtools',
    'crispy_forms',
]

LOCAL_APPS = [
    'app_dir.account',
    'app_dir.permit',
    'app_dir.address',
]

# Applications definition
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app_dir.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
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

WSGI_APPLICATION = 'app_dir.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', default='django.db.backends.postgresql'),
        'NAME': env('DATABASE_NAME', default=''),
        'USER': env('DATABASE_USERNAME', default=''),
        'PASSWORD': env('DATABASE_PASSWORD', default=''),
        'HOST': env('DATABASE_HOST', default=''),
        'PORT': env('DATABASE_PORT', default='')
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

if DEBUG is False:
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
else:
    AUTH_PASSWORD_VALIDATORS = []  # hate it locally


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = env(
    "DJANGO_STATIC_ROOT",
    default=str(ROOT_DIR('../var/static_root'))
)

STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = str(ROOT_DIR('media'))

# Configuration for apps
FIXTURE_DIRS = (
    str(ROOT_DIR('fixtures')),
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Redirect to page after login
LOGIN_REDIRECT_URL = '/'


# if we have sentry credentials - use it
RAVEN_DSN = env("RAVEN_DSN", default=None)
if RAVEN_DSN:
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
    }

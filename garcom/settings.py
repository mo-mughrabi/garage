import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        os.path.pardir))


def base(f):
    return os.path.join(BASE_DIR, f)


def app_base(f=''):
    return os.path.join(base('garcom'), f)


# append to python PATH
sys.path.insert(0, app_base())

ADMINS = (
    ('User', 'email'),  # user and email address of admins
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Kuwait'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'
ADMIN_LANGUAGE_CODE = LANGUAGE_CODE

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
)

SITE_ID = 1

DEBUG = True
TEMPLATE_DEBUG = DEBUG


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = base('public_media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/public_media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = base('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    app_base('frontend'),
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'j!(9=8v_p47qqh0r+_e6wkw7yhyd4*(he*(#g^6u@!0jdx^id9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'misc.middleware.MinifyHTMLMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# APPEND_SLASH = False
ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

# LOCALE Path
LOCALE_PATHS = (
    app_base('misc/locale'),
)

TEMPLATE_CONTEXT_PROCESSORS = (

    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

TEMPLATE_DIRS = (
    app_base('misc/templates'),
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'hvad',
    'captcha',
    'storages',
    'djcelery',
    'social_auth',
    'django_ses',
    'south',
    'sorl.thumbnail',
    'rest_framework',
    #'djgo_translator',
    'dj_dba',
    # garage apps
    'misc.common_lib',
    'apps.accounts',
    'apps.vehicle',
    'apps.pages',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': None
}


# Email Configuration using Amazon SES Services
EMAIL_BACKEND = 'django_ses.SESBackend'

# These are optional -- if they're set as environment variables they won't
# need to be set here as well
AWS_SES_ACCESS_KEY_ID = ''  # AWS Key
AWS_SES_SECRET_ACCESS_KEY = ''  # AWS Secret

# Additionally, you can specify an optional region, like so:
AWS_SES_REGION_NAME = 'us-east-1'
# AWS_SES_REGION_ENDPOINT = 'email-smtp.us-east-1.amazonaws.com'
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

OUTGOING_EMAILS = 'noreply@yourdomain.com'


# minify html output
COMPRESS_HTML = False



# Garage Configuration
GARAGE_INDIV_INITIAL_PHONES = 1
GARAGE_INDIV_MAX_PHONES = 10
GARAGE_INDIV_INITIAL_PAYMENTS = 1
GARAGE_INDIV_MAX_PAYMENTS = 5

# Password recovery settings
GARAGE_PASS_PHRASE_LENGTH = 15
GARAGE_PASS_PHRASE_EXPIRY = 2  # expiry in hours
GARAGE_PASSWORD_LENGTH = 8


# Celery
import djcelery
djcelery.setup_loader()
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = ""
BROKER_PASSWORD = ""
BROKER_VHOST = ""

CELERY_BACKEND = "amqp"
CELERY_RESULT_BACKEND = "amqp"


AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuthBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    "misc.backend_auth.EmailAuthBackend",
)

SOCIAL_AUTH_ASSOCIATE_BY_MAIL = True
SOCIAL_AUTH_CREATE_USER = True


# Google OAuth Key for authentication
GOOGLE_OAUTH2_CLIENT_ID = ''  # google client ID for social auth
GOOGLE_OAUTH2_CLIENT_SECRET = ''  # google client secret for social auth
# Facebook OAuth Keys
FACEBOOK_APP_ID = ''  # facebook app id for social auth
FACEBOOK_API_SECRET = ''  # facebook app secret for social auth
FACEBOOK_EXTENDED_PERMISSIONS = ['email', ]
FACEBOOK_EXTRA_DATA = [
    ('email', 'email'),
]

# linked in authentication
LINKEDIN_CONSUMER_KEY = ''  # linkedin consumer key for socil auth
LINKEDIN_CONSUMER_SECRET = ''  # linkedin consumer secret for social auth
LINKEDIN_SCOPE = ['r_emailaddress', ]
LINKEDIN_EXTRA_FIELD_SELECTORS = ['email-address', ]
LINKEDIN_EXTRA_DATA = [('email-address', 'email_address'), ]


# github
GITHUB_APP_ID = ''  # github app id for social auth
GITHUB_API_SECRET = ''  # github app secret for social auth

# Google API KEY used for DJGO_TRANSLATOR
GOOGLE_API_KEY = ''  # google api key / only required when running translations


# Account Management
LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/account/'
LOGIN_ERROR_URL = '/account/auth-error/'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'first_name', 'last_name']

AUTH_PROFILE_MODULE = 'accounts.Profile'


# reCAPTCHA settings
RECAPTCHA_PUBLIC_KEY = ''  # recaptcha key
RECAPTCHA_PRIVATE_KEY = ''  # recaptcaha private key


# DJ_DBA
DJ_DBA_DEFAULT_FIXTURES = (
    base('garcom/apps/accounts/fixtures/users.json'),
    base('garcom/apps/pages/fixtures/faq.json'),
)

DJ_DBA_POST_FIXTURE_COMMANDS = (
    'migrate',
    'load_model_lookup_from_vehicle_db',
    'load_colors',
)


# WATERMARK
WATERMARK_IMAGE = base('garcom/frontend/apps/vehicle/img/overlay.png')

try:
    from misc.setting_templates.local_env import *
except ImportError:
    pass

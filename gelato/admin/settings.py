# -*- coding: utf-8 -*-
# Django settings for zamboni project.

import os
import logging
import socket

from django.utils.functional import lazy
from metlog.config import client_from_dict_config

WAFFLE_TABLE_SUFFIX = 'amo'
LOG_TABLE_SUFFIX = ''
EVENT_TABLE_SUFFIX = ''

try:
    # If we have build ids available, we'll grab them here and add them to our
    # CACHE_PREFIX.  This will let us not have to flush memcache during updates
    # and it will let us preload data into it before a production push.
    from build import BUILD_ID_CSS, BUILD_ID_JS
    build_id = "%s%s" % (BUILD_ID_CSS[:2], BUILD_ID_JS[:2])
except ImportError:
    build_id = ""

# Make filepaths relative to the root of zamboni.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = lambda *a: os.path.join(ROOT, *a)

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True

# LESS CSS OPTIONS (Debug only)
LESS_PREPROCESS = False  # Compile LESS with Node, rather than client-side JS?
LESS_LIVE_REFRESH = False  # Refresh the CSS on save?
LESS_BIN = 'lessc'

# Path to uglifyjs. When not None, this will be used to minify JavaScript
# instead of YUI.
UGLIFY_BIN = None

DATABASES = {
    'default': {
        'NAME': 'zamboni',
        'ENGINE': 'mysql_pymysql',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
        'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    },
}


DATABASE_ROUTERS = ('multidb.PinningMasterSlaveRouter',)

# For use django-mysql-pool backend.
DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 5,
    'recycle': 300
}

# Put the aliases for your slave databases in this list.
SLAVE_DATABASES = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Accepted locales
# Note: If you update this list, don't forget to also update the locale
# permissions in the database.
AMO_LANGUAGES = (
    'af', 'ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en-US', 'es', 'eu', 'fa',
    'fi', 'fr', 'ga-IE', 'he', 'hu', 'id', 'it', 'ja', 'ko', 'mn', 'nl', 'pl',
    'pt-BR', 'pt-PT', 'ro', 'ru', 'sk', 'sl', 'sq', 'sv-SE', 'uk', 'vi',
    'zh-CN', 'zh-TW',
)

# Explicit conversion of a shorter language code into a more specific one.
SHORTER_LANGUAGES = {
    'en': 'en-US', 'ga': 'ga-IE', 'pt': 'pt-PT', 'sv': 'sv-SE', 'zh': 'zh-CN'
}

# Not shown on the site, but .po files exist and these are available on the
# L10n dashboard.  Generally languages start here and move into AMO_LANGUAGES.
HIDDEN_LANGUAGES = ('cy', 'sr', 'sr-Latn', 'tr')


def lazy_langs(languages):
    from product_details import product_details
    if not product_details.languages:
        return {}
    return dict([(i.lower(), product_details.languages[i]['native'])
                 for i in languages])

# Where product details are stored see django-mozilla-product-details
PROD_DETAILS_DIR = path('product_json')

# Override Django's built-in with our native names
LANGUAGES = lazy(lazy_langs, dict)(AMO_LANGUAGES)
RTL_LANGUAGES = ('ar', 'fa', 'fa-IR', 'he')

LANGUAGE_URL_MAP = dict([(i.lower(), i) for i in AMO_LANGUAGES])

# Tower / L10n
LOCALE_PATHS = (path('locale'),)
TEXT_DOMAIN = 'messages'
STANDALONE_DOMAINS = [TEXT_DOMAIN, 'javascript']
TOWER_KEYWORDS = {
    '_lazy': None,
}
TOWER_ADD_HEADERS = True

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# The host currently running the site.  Only use this in code for good reason;
# the site is designed to run on a cluster and should continue to support that
HOSTNAME = socket.gethostname()

# The front end domain of the site. If you're not running on a cluster this
# might be the same as HOSTNAME but don't depend on that.  Use this when you
# need the real domain.
DOMAIN = HOSTNAME

# Full base URL for your main site including protocol.  No trailing slash.
#   Example: https://addons.mozilla.org
SITE_URL = 'http://%s' % DOMAIN

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to a temporary storage area
TMP_PATH = path('tmp')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    path('templates'),
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

# Auth
AUTHENTICATION_BACKENDS = (
    'gelato.models.users.AmoUserBackend',
)
AUTH_PROFILE_MODULE = 'users.UserProfile'

ROOT_URLCONF = 'gelato.admin.urls'

INSTALLED_APPS = (
    'gelato.admin',
    'addons',
    'gelato.translations',
    'translations',
    'applications',
    'versions',
    'users',
    'django_extensions',
    'django_nose',
    'raven.contrib.django',
    'waffle',

    # Django contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
)

# These apps will be removed from INSTALLED_APPS in a production environment.
DEV_APPS = (
    'django_nose',
)

# Tests
TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'
NOSE_ARGS = [
    '--with-fixture-bundling',
    '--exclude=mkt/*',
]


# Caching
# Prefix for cache keys (will prevent collisions when running parallel copies)
CACHE_PREFIX = 'amo:%s:' % build_id
KEY_PREFIX = CACHE_PREFIX
FETCH_BY_ID = True

# Number of seconds a count() query should be cached.  Keep it short because
# it's not possible to invalidate these queries.
CACHE_COUNT_TIMEOUT = 60

STATIC_URL = SITE_URL

# Outgoing URL bouncer
REDIRECT_URL = 'http://outgoing.mozilla.org/v1/'
REDIRECT_SECRET_KEY = ''

# Allow URLs from these servers. Use full domain names.
REDIRECT_URL_WHITELIST = ['addons.mozilla.org']

# Default to short expiration; check "remember me" to override
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_DOMAIN = ".%s" % DOMAIN  # bug 608797
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Logging
LOG_LEVEL = logging.DEBUG
# See PEP 391 and log_settings.py for formatting help.  Each section of
# LOGGING will get merged into the corresponding section of
# log_settings.py. Handlers and log levels are set up automatically based
# on LOG_LEVEL and DEBUG unless you set them here.  Messages will not
# propagate through a logger unless propagate: True is set.
LOGGING_CONFIG = None
LOGGING = {
    'loggers': {
        'caching.invalidation': {'handlers': ['null']},
        'caching': {'level': logging.WARNING},
        'z.es': {'level': logging.INFO},
        'nose': {'level': logging.WARNING},
    },
}


METLOG_CONF = {
    'logger': 'zamboni',
    'plugins': {'cef': ('metlog_cef.cef_plugin:config_plugin', {})},
    'sender': {
        'class': 'metlog.senders.logging.StdLibLoggingSender',
        'logger_name': 'z.metlog',
    },
}

METLOG = client_from_dict_config(METLOG_CONF)

# Send Django signals asynchronously on a background thread.
ASYNC_SIGNALS = True

# Feature flags
SEARCH_EXCLUDE_PERSONAS = True


## elasticsearch
ES_HOSTS = ['127.0.0.1:9200']
ES_INDEXES = {'default': 'amo',
              'update_counts': 'amo_stats',
              'download_counts': 'amo_stats',
              'stats_contributions': 'amo_stats',
              'stats_collections_counts': 'amo_stats',
              'users_install': 'amo_stats'}
ES_TIMEOUT = 30

# Super temporary.
MARKETPLACE = False
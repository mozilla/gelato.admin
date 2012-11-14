import private
from gelato.admin.settings import *

HOSTNAME='marketplace-admin-dev.allizom.org'
DOMAIN=HOSTNAME
SITE_URL = 'http://%s' % DOMAIN
STATIC_URL = SITE_URL

DATABASES = {
    'default': {
        'ENGINE': 'mysql_pymysql',
        'NAME': private.DATABASES_DEFAULT_NAME,
        'HOST': private.DATABASES_DEFAULT_HOST,
        'PORT': private.DATABASES_DEFAULT_PORT,
        'USER': private.DATABASES_DEFAULT_USER,
        'PASSWORD': private.DATABASES_DEFAULT_PASSWORD,
        'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    },
}

SESSION_COOKIE_DOMAIN = ".%s" % HOSTNAME

import dj_database_url

import private
from gelato.admin.settings import *

HOSTNAME = 'marketplace-admin-dev.allizom.org'
DOMAIN = HOSTNAME
SITE_URL = 'http://%s' % DOMAIN
STATIC_URL = SITE_URL

DATABASES = {'default': dj_database_url.parse(private.DATABASES_DEFAULT_URL)}
DATABASES['default'].update({
    'ENGINE': 'mysql_pymysql',
    'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
    'TEST_CHARSET': 'utf8',
    'TEST_COLLATION': 'utf8_general_ci',
})

SESSION_COOKIE_DOMAIN = ".%s" % HOSTNAME

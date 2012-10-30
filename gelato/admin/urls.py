from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

import gelato.admin.admin
gelato.admin.admin.register()

urlpatterns = patterns('',
    url(r'^adm/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()

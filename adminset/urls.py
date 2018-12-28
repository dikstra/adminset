from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from adminset.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^cmdb/', include('cmdb.urls')),
    url(r'^navi/', include('navi.urls')),
    url(r'^monitor/', include('monitor.urls')),
    url(r'^webssh/', include('webssh.urls')),
    url(r'^accounts/', include('accounts.urls')),
]
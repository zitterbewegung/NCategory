from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from mrfantastic.base import views as base_views
from mrfantastic.simplex import views as simplex_views

urlpatterns = [
    url(r'^$', base_views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),

    # contribute.json url
    url(r'^(?P<path>contribute\.json)$', 'django.views.static.serve',
        {'document_root': settings.ROOT}),
]

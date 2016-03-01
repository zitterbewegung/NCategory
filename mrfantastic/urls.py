from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from mrfantastic.base import views as base_views
from mrfantastic.simplex import views as simplex_views

router = routers.DefaultRouter()
# register job endpoint in the router
router.register(r'jobs', simplex_views.JobViewSet)

urlpatterns = [
    url(r'^$', base_views.home, name='home'),
    url(r'^router/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'search/', base_views.search, name='search'), 
    # contribute.json url
    url(r'^(?P<path>contribute\.json)$', 'django.views.static.serve',
        {'document_root': settings.ROOT}),
]

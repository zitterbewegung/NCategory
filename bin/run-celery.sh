#!/bin/sh
# From https://www.syncano.io/blog/configuring-running-django-celery-docker-containers-pt-1/
cd myproject
# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m myuser -c "celery worker -A myproject.celeryconf -Q default -n default@%h"

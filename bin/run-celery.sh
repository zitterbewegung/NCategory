#!/bin/bash
# From https://www.syncano.io/blog/configuring-running-django-celery-docker-containers-pt-1/

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
celery worker -A mrfantastic.simplex.celeryconf -Q default -n default@%h

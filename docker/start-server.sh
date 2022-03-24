#!/bin/bash
# start-server.sh
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (cd bookapi; python manage.py createsuperuser --email $DJANGO_SUPERUSER_EMAIL --no-input)
fi
cd bookapi
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
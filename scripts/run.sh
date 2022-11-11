#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket 0.0.0.0:${API_SERVICE_PORT} --workers 4 --master --enable-threads --module server.wsgi
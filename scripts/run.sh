#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --http 0.0.0.0:9000 --workers 4 --master --enable-threads --module server.wsgi
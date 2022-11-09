#!/bin/sh
docker-compose run --rm src sh -c "python manage.py test"

#!/bin/sh
docker-compose run --rm src sh -c "coverage run manage.py test"
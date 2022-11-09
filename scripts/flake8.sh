#!/bin/sh
docker-compose run --rm src sh -c "flake8 --exclude=core/migrations/"
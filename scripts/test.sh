coverage run manage.py test
coverage report
flake8 --exclude=core/migrations/
/py/bin/pip uninstall -r /requirements/requirements.dev.txt
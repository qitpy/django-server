sudo /py/bin/pip install -r /requirements/requirements.dev.txt
coverage run manage.py test
coverage report
flake8 --exclude=core/migrations/
sudo /py/bin/pip uninstall -r /requirements/requirements.dev.txt

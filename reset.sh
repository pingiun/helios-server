#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.
dropdb helios
createdb helios
python manage.py makemigrations
python manage.py migrate
python manage.py createadmin

#!/bin/bash
python manage.py wait_for_db


python3 manage.py makemigrations
python3 manage.py migrate

exec python3 manage.py runserver 0.0.0.0:8000

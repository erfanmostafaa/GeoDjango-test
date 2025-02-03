#!/bin/bash

echo "Waiting for database to be ready..."
python3 manage.py wait_for_db

echo "Applying migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Starting Django server..."
exec python3 manage.py runserver 0.0.0.0:8000

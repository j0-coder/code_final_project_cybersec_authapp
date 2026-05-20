#!/bin/sh

until pg_isready -h "$SECRET_HOST" -p "$SECRET_PORT"; do
    echo "Waiting for Postgres to initialize..."
    sleep 10
done

cd AuthApp
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8080
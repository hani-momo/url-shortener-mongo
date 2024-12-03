#!/bin/sh

echo "Waiting for MongoDB to be ready..."
while ! nc -z mongo 27017; do
  sleep 0.1
done

echo "Applying migrations..."
python manage.py migrate

echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

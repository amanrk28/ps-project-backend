#!/bin/sh

python manage.py migrate

if [ "$ENVIRONMENT" = "production" ]; then
  python manage.py collectstatic --no-input;
  gunicorn --timeout 120 --workers=4 --bind=0.0.0.0:80 project_backend.wsgi
elif [ "$ENVIRONMENT" = "development" ]; then
  python manage.py collectstatic --no-input;
  python manage.py runserver 0.0.0.0:8000
fi
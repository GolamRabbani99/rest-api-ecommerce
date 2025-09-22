#!/usr/bin/env bash

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Start the web server
gunicorn ecommerce_api.wsgi:application --bind 0.0.0.0 --timeout 600

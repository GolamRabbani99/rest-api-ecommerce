#!/usr/bin/env bash
# Exit on first error
set -e

python manage.py makemigrations
python manage.py migrate

#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput

# Apply database migrations
#echo "Apply database migrations"
#python manage.py migrate

# Start server
echo "Starting server"
python3 manage.py runserver 127.0.0.1:8000
#!/bin/bash
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
# Apply backend fixtures
echo "Apply fixtures"
python manage.py loaddata backend/fixtures/params_fixture.json
# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
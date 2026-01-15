#!/bin/bash

set -e

# Run database migrations if needed
echo "Setting up Flask app..."

# Start gunicorn
exec gunicorn \
    --bind 0.0.0.0:8080 \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    "app:create_app()"

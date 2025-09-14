#!/bin/bash

# Production startup script for AnNi AI HR Platform
echo "Starting AnNi AI HR Platform in production mode..."

# Change to the backend source directory
cd /opt/render/project/src/backend/src

# Start Gunicorn with configuration
exec gunicorn --config ../gunicorn_config.py main:app


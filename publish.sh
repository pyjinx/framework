#!/bin/bash

set -e # Exit script immediately on first error

# Check if .env file exists
if [ -f .env ]; then
  # Read and export variables from .env file
  export $(cat .env | xargs)
fi

# Clean package directories if they exist
[ -d dist ] && rm -rf dist

# Remove all .egg-info directories if they exist
find . -name "*.egg-info" -type d -exec rm -rf {} +

# Clean all __pycache__ directories
find . -name "__pycache__" -type d -exec rm -rf {} +

# Publish package using Twine
poetry publish --username "$PYPI_USERNAME" --password "$PYPI_PASSWORD" --build

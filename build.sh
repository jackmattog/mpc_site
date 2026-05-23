#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Node.js dependencies (To get Tailwind working)
npm install

# Build Tailwindcss
npm run build

# Install dependencies
pip install -r requirements.txt


# Run database migrations
python manage.py migrate

# Collect static files for Tailwind/CSS
python manage.py collectstatic --no-input
#!/bin/bash
# Usage: format_db.sh <user> <email>
# The command prompts for password
workon rn-django17
echo "==> Creating super user $1"
python manage.py createsuperuser --user $1 --email $2
echo "==> Creating database"
python manage.py migrate
echo "==> Creating Quartiers, Storerooms, .."
python stock_assign/initialization.py
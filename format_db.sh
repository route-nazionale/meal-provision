#!/bin/bash
# Usage: format_db.sh <user> <email>
# The command prompts for password
workon rn-django17
echo "==> Creating database"
python manage.py migrate
echo "==> Creating Quartiers, Storerooms, .."
echo -e "from stock_assign.initialization import * \npopulate_db() \nquit()" | python manage.py shell
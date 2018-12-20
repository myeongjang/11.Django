#!/bin/sh

virtualenv -p python3 env
. ./env/bin/activate
pip install django
cd bug
./manage.py bootstrap

echo 'And now try to create Bravo
from app.models import Bravo
Bravo.objects.create()
... snip ...
django.db.utils.OperationalError: no such table: main.app_alpha__old
'

./manage.py shell


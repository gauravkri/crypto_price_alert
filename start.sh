#!/bin/bash 

python3 manage.py makemigrations alertApp

python3 manage.py migrate 

python manage.py runserver &>/tmp/srvr.log &

celery -A pricealertproject worker -l info &
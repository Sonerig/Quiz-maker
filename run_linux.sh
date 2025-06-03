#!/bin/bash

if [ ! -d venv ]; then
    python -m venv venv
    venv/bin/pip install -r requirements.txt
    venv/bin/python quiz_maker/manage.py migrate
fi
source venv/bin/activate
cd quiz_maker; python manage.py runserver
#!/bin/bash

if [ ! -d venv ]; then
    python -m venv venv
    venv/bin/pip install -r requirements.txt
fi
source venv/bin/activate
cd quiz_maker; python -m uvicorn quiz_maker.asgi:application --host 127.0.0.1 --port 8000
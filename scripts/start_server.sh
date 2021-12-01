#!/bin/bash
export USER_SERVICE_DIR=$(pwd)
export PYTHONPATH="${USER_SERVICE_DIR}/app"
export FLASK_APP="app.py"
cd "${USER_SERVICE_DIR}/app"
gunicorn --chdir $USER_SERVICE_DIR wsgi:app -w 4 -k gevent -b 0.0.0.0:5000 -t 60

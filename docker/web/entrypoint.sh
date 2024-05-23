#!/usr/bin/env bash

if [ $# -eq 0 ]
then
  exec gunicorn -b 0.0.0.0:8000 -w 4 project.wsgi
else
  exec python3 manage.py $@
fi

#!/usr/bin/env bash

if [ $# -eq 0 ]
then
  exec python3 manage.py runserver 0.0.0.0:8000
else
  exec python3 manage.py $@
fi

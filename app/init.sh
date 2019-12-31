#!/bin/bash

python3 init_db.py

gunicorn -b "0.0.0.0:8000" app:app
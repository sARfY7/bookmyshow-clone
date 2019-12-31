#!/bin/bash

echo "Creating Tables"
python3 create_db.py
echo "Tables created"

gunicorn -b "0.0.0.0:8000" app:app
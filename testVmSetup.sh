#!/bin/bash
cd ~/../Immunome/mysite
echo -n "Actual Python Version: "
python --version
echo "Expected Python Version: Python 3.6.3"
echo -n "Actual Django Version: "
python -m django --version
echo "Expected Django Version: 2.2.7"
python manage.py runserver

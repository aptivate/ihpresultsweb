#!/bin/sh
command=$1
cd /home/burgercom/ihp.burgercom.co.za/ihp
source /home/burgercom/.virtualenvs/ihp/bin/activate
echo "`date` ${command}" >> log
python manage.py ${command}

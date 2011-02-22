#!/bin/sh
# script used by cron to pull mail and any other maintenance tasks
# This script is going to be deleted in March 2011 as there is no longer a need to accept submissions via email

command=$1
cd /home/burgercom/ihp.burgercom.co.za/ihp
source /home/burgercom/.virtualenvs/ihp/bin/activate
echo "`date` ${command}" >> log
python manage.py ${command} --settings=ihp.settings_prod

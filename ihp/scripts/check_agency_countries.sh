#!/bin/sh

cd /home/burgercom/ihp.burgercom.co.za/ihp
source /home/burgercom/.virtualenvs/ihp/bin/activate
echo `date` >> log
python manage.py loadagencycountries

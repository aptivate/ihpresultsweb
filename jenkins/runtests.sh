#!/bin/sh
# this script is for jenkins to use to run itself
/usr/bin/virtualenv --no-site-packages --python /usr/bin/python2.6 --distribute env
env/bin/pip-2.6 install -E env -r deploy/pip_packages.txt 
env/bin/pip-2.6 install -E env MySQL-python

cd ihp/
if [ ! -f local_settings.py ]; then
  /bin/ln -s local_settings.py.jenkins local_settings.py
  # the git version does not have local_settings import
  echo "from local_setttings import *" >> local_settings.py
fi
cd -

env/bin/python2.6 ihp/manage.py syncdb --noinput
env/bin/python2.6 ihp/manage.py migrate --noinput
env/bin/python2.6 ihp/manage.py jenkins --pylint-rcfile=jenkins/pylint.rc publicweb


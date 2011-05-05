import site
site.addsitedir('lib/python2.6/site-packages')

import os
import sys

project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(project_dir, '..')))
sys.path.append(os.path.abspath(os.path.join(project_dir, '../ihp/')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ihp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

from dozer import Dozer
application = Dozer(application)

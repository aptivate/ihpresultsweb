import sys, os
os.environ["DJANGO_SETTINGS_MODULE"] = "ihp.settings"

INTERP = os.path.join(os.environ["HOME"], ".virtualenvs", "ihp", "bin", "python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

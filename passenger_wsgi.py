import sys, os
os.environ["DJANGO_SETTINGS_MODULE"] = "ihp.settings_prod"

INTERP = os.path.join(os.environ["HOME"], ".virtualenvs", "ihp", "bin", "python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
cwd = os.getcwd()

sys.path.append(os.getcwd())
sys.path.append(os.path.join(cwd, "ihp"))
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

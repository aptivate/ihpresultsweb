import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ihp import local_settings

db_user = 'nouser'
db_pw   = 'nopass'
# there are two ways of having the settings:
# either as DATABASE_NAME = 'x', DATABASE_USER ...
# or as DATABASES = { 'default': { 'NAME': 'xyz' ... } }
try:
    db = local_settings.DATABASES
    db_engine = db['default']['ENGINE']
    db_name   = db['default']['NAME']
    if db_engine == 'mysql':
        db_user   = db['default']['USER']
        db_pw     = db['default']['PASSWORD']
except:
    try:
        db_engine = local_settings.DATABASE_ENGINE
        db_name   = local_settings.DATABASE_NAME
        if db_engine == 'mysql':
            db_user   = local_settings.DATABASE_USER
            db_pw     = local_settings.DATABASE_PASSWORD
    except:
        # we've failed to find the details we need - give up
        sys.exit(1)

print("%s %s %s %s" % (db_engine, db_name, db_user, db_pw))

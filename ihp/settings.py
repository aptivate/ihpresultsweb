import os

PROJECT_HOME = os.path.dirname(os.path.realpath(__name__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Adi Eyal', 'adi@burgercom.co.za'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3' 
DATABASE_NAME = 'ihp.db'

TIME_ZONE = 'Africa/Johannesburg'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_HOME, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'z4q!x3&rq^ex1udn)e3w0*zlr_pqe4ecpe9#il%d!$k%4@eew('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'ihp.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_HOME, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
   
    'submissions',
)

# Poll Email Account Settings
#POLL_USERNAME = "ihp@burgercom.co.za"
#POLL_PASSWORD = "paddycake"
POLL_USERNAME = "ihpresults2010survey@human-scale.net"
POLL_PASSWORD = "changeme"
POLL_HOST = "pop.gmail.com"

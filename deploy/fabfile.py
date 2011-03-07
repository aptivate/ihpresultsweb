from fabric.api import *
from fabric import utils
from fabric.decorators import hosts

# this is our common file that can be copied across projects
# we deliberately import all of this to get all the commands it
# provides as fabric commands
from fablib import *
import fablib


env.home = '/var/django/'
env.project = 'reactionscorecards3'
env.repo_type = 'git'
env.repository = 'git://github.com/aptivate/ihpresultsweb.git'
env.django_apps = ['publicweb', 'submissions', ]
env.test_cmd = ' manage.py test -v0 ' + ' '.join(env.django_apps)

#
# These three commands set up the environment variables
# to be used by later commands
#

def _local_setup():
    fablib._setup_path()
    env.django_root = os.path.join(env.vcs_root, 'ihp')

def staging_test():
    """ use staging environment on remote host to run tests"""
    utils.abort('need to refactor fabfile for this to work')
    # this is on the same server as the customer facing stage site
    # so we need project_root to be different ...
    env.project_subdir = env.project + '_test'
    env.environment = 'staging_test'
    env.hosts = ['fen-vz-osiaccounting']
    _local_setup()

def dev():
    """ use staging environment on remote host to demo to client"""
    env.environment = 'dev_server'
    env.hosts = ['lin-reactionscorecards3-dev.aptivate.org:48001']
    _local_setup()

def staging():
    """ use staging environment on remote host to demo to client"""
    env.environment = 'staging'
    env.hosts = ['lin-reactionscorecards3-stage.aptivate.org:48001']
    _local_setup()

def production():
    """ use production environment on remote host"""
    env.environment = 'production'
    env.hosts = ['lin-reactionscorecards3-live.aptivate.org:48001']
    _local_setup()

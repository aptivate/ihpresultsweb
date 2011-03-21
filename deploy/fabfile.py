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

# the top level directory on the server
env.project_dir = env.project

# repository type can be "svn" or "git"
env.repo_type = 'git'
env.repository = 'git://github.com/aptivate/ihpresultsweb.git'

env.django_dir = env.project
env.django_apps = ['publicweb', 'submissions', ]
env.test_cmd = ' manage.py test -v0 ' + ' '.join(env.django_apps)

# put "django" here if you want django specific stuff to run
# put "plain" here for a basic apache app
env.project_type = "django"

# does this virtualenv for python packages
env.use_virtualenv = True

# valid environments - used for require statements in fablib
env.valid_non_prod_envs = ('dev_server', 'staging_test', 'staging')
env.valid_envs = ('dev_server', 'staging_test', 'staging', 'production')
env.use_apache = True

# this function can just call the fablib _setup_path function
# or you can use it to override the defaults
def _local_setup():
    # put your own defaults here
    fablib._setup_path()
    # override settings here
    # if you have an ssh key and particular user you need to use
    # then uncomment the next 2 lines
    #env.user = "root" 
    #env.key_filename = ["/home/shared/keypair.rsa"]
    env.django_root = os.path.join(env.vcs_root, 'ihp')

#
# These commands set up the environment variables
# to be used by later commands
#

def dev():
    """ use dev environment on remote host to play with code in production-like env"""
    env.environment = 'dev_server'
    env.hosts = ['lin-reactionscorecards3-dev.aptivate.org:48001']
    _local_setup()


def staging_test():
    """ use staging environment on remote host to run tests"""
    # this is on the same server as the customer facing stage site
    # so we need project_root to be different ...
    env.project_dir = env.project + '_test'
    env.environment = 'staging_test'
    env.hosts = ['lin-reactionscorecards3-stage.aptivate.org:48001']
    env.use_apache = False
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

def deploy():
    fablib.deploy()
    cache_dir = os.path.join(env.vcs_root, 'wordpress', 'wp-content',
        'plugins', 'wp-minify', 'cache')
    sudo('mkdir -p ' + cache_dir)
    sudo('chmod a+w ' + cache_dir)
    upload_dir = os.path.join(env.vcs_root, 'wordpress', 'wp-content',
        'uploads')
    sudo('mkdir -p ' + upload_dir)
    sudo('chown -R apache ' + upload_dir)

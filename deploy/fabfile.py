import os
import getpass

from fabric.api import *
from fabric.contrib import files, console
from fabric.contrib.files import exists
from fabric import utils
from fabric.decorators import hosts

# based on
# http://www.caktusgroup.com/blog/2010/04/22/basic-django-deployment-with-virtualenv-fabric-pip-and-rsync/


env.home = '/var/django/'
env.project = 'reactionscorecards3'
env.repository = 'https://svn.aptivate.org/svn/' + env.project + '/dev'
env.svnuser = 'redmine'
env.svnpass = 'redm1ne2010svn'
env.django_test_apps = ['accounts', ]
env.test_cmd = ' manage.py test -v0 ' + ' '.join(env.django_test_apps)

def _setup_path():
    env.project_root    = os.path.join(env.home, env.project)
    env.svn_root        = os.path.join(env.project_root, 'dev')
    env.django_root     = os.path.join(env.svn_root, env.project)
    env.virtualenv_root = os.path.join(env.project_root, 'env')
    env.python_bin      = os.path.join(env.virtualenv_root, 'bin', 'python26')
    env.settings        = '%(project)s.settings' % env

def _get_svn_user_and_pass():
    # just use the redmine user for now.
    pass
#    if len(env.svnuser) == 0:
#      # prompt user for username
#      prompt('Enter SVN username:', 'svnuser')
#    if len(env.svnpass) == 0:
#      # prompt user for password
#      env.svnpass = getpass.getpass('Enter SVN password:')


def staging():
    """ use staging environment on remote host"""
    #env.user = 'apache'
    env.environment = 'staging'
    env.hosts = ['lin-reactionscorecards3-stage.aptivate.org:48001']
    _setup_path()


def production():
    """ use production environment on remote host"""
    utils.abort("not ready yet")
    env.environment = 'production'
    env.hosts = ['lin-osiacct.aptivate.org:48001']
    _setup_path()


def deploy_clean():
    """ delete the entire install and do a clean install """
    require('project_root', provided_by=('staging', ))
    if env.environment == 'production':
        utils.abort('do not delete the production environment!!!')
    sudo('rm -rf %s' % env.project_root)


def deploy_initial():
    """ initialize remote host environment (virtualenv, deploy, update) """
    require('project_root', provided_by=('staging', 'production'))
    sudo('mkdir -p %(project_root)s' % env)
    create_virtualenv()
    checkout_or_update()
    update_requirements()
    create_db()
    link_apache_conf()
    apache_restart()


def deploy_updates():
    """ update remote host environment (virtualenv, deploy, update) """
    require('project_root', provided_by=('staging', 'production'))
    if not files.exists(env.project_root):
        utils.abort('No initial deploy - do \$ fab %s deploy_initial' %
            env.environment)
    sudo('mkdir -p %(project_root)s' % env)
    checkout_or_update()
    update_requirements()
    update_db()
    link_apache_conf()
    apache_restart()


def local_test():
    """ run the django tests on the local machine """
    with cd(os.path.join("..", env.project)):
        local("python " + env.test_cmd, capture=False)


def remote_test():
    """ run the django tests remotely - staging only """
    require('django_root', provided_by=('staging', ))
    require('python_bin', provided_by=('staging', ))
    require('test_cmd', provided_by=('staging', ))
    with cd(env.django_root):
        sudo(env.python_bin + env.test_cmd)


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=('staging', 'production'))
    if files.exists(os.path.join(env.virtualenv_root, 'bin')):
        utils.warn('virtualenv already exists - please use deploy_updates rather than deploy_initial')
        return
    # note these args are for centos 5 as set up by puppet
    args = '--clear --python /usr/bin/python26 --no-site-packages --distribute'
    sudo('virtualenv %s %s' % (args, env.virtualenv_root))


def checkout_or_update():
    """ checkout the project from subversion """
    require('project_root', provided_by=('staging', 'production'))
    require('svn_root', provided_by=('staging', 'production'))
    require('django_root', provided_by=('staging', 'production'))
    require('repository', provided_by=('staging', 'production'))
    # function to ask for svnuser and svnpass
    _get_svn_user_and_pass()
    # if the .svn directory exists, do an update, otherwise do
    # a checkout
    if files.exists(os.path.join(env.svn_root, ".svn")):
        with cd(env.svn_root):
            sudo('svn update --username %s --password %s' % 
                (env.svnuser, env.svnpass))
    else:
        with cd(env.project_root):
            sudo('svn checkout --username %s --password %s %s' % 
                (env.svnuser, env.svnpass, env.repository))
    # ensure that we create a local_settings.py using a link
    # eg. 'ln -s local_settings.py.staging local_settings.py'
    local_settings_path = os.path.join(env.django_root, 'local_settings.py')
    if not files.exists(local_settings_path):
        with cd(env.django_root):
            sudo('ln -s local_settings.py.' + env.environment + ' local_settings.py')
    # touch the wsgi file to reload apache
    touch()


def update_requirements():
    """ update external dependencies on remote host """
    require('svn_root', provided_by=('staging', 'production'))
    require('virtualenv_root', provided_by=('staging', 'production'))

    cmd_base = ['source %(virtualenv_root)s/bin/activate; ' % env]
    cmd_base += ['pip install']
    cmd_base += ['-E %(virtualenv_root)s' % env]

    cmd = cmd_base + ['--requirement %s' % os.path.join(env.svn_root, 'deploy', 'pip_packages.txt')]
    sudo(' '.join(cmd))

    # mysql is not normally installed on development machines,
    # let's ensure it is installed
    cmd = cmd_base + ['MySQL-python']
    sudo(' '.join(cmd))


def create_db():
    """ create the database, user and password """
    print ("create_db not implemented yet")
    # TODO: 
    # with cd(env.django_root):
    # sudo(env.python_path + ' manage.py syncdb --migrate')

def update_db():
    """ update the database, do migrations etc """
    print ("update_db not implemented yet")
    # TODO: 

def touch():
    """ touch wsgi file to trigger reload """
    require('svn_root', provided_by=('staging', 'production'))
    wsgi_dir = os.path.join(env.svn_root, 'wsgi')
    sudo('touch ' + os.path.join(wsgi_dir, 'wsgi_handler.py'))


def link_apache_conf():
    """link the apache.conf file"""
    require('svn_root', provided_by=('staging', 'production'))
    conf_file = os.path.join(env.svn_root, 'apache', env.environment+'.conf')
    apache_conf = os.path.join('/etc/httpd/conf.d', env.project+'-stage.conf')
    if not files.exists(conf_file):
        utils.abort('No apache conf file found - expected %s' % conf_file)
    if not files.exists(apache_conf):
        sudo('ln -s %s %s' % (conf_file, apache_conf))
    configtest()


def configtest():    
    """ test Apache configuration """
    sudo('/usr/sbin/httpd -S')


def apache_reload():    
    """ reload Apache on remote host """
    sudo('/etc/init.d/httpd reload')


def apache_restart():    
    """ restart Apache on remote host """
    sudo('/etc/init.d/httpd restart')




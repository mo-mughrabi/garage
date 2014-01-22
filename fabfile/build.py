from misc import virtualenv, git, git_pull
import datetime
from fabric.api import env, run
from fabric.context_managers import cd
from daemons import restart_uwsgi, restart_celery
from sys import exit
from fabric.contrib.files import exists


def who():
    """
    """
    run('who')


def build_cars_base(arg):
    ''' this function will cars into the database randomly based on the number given in the args '''
    if not env.hosts:
        print 'Error: must use enviroment (e.g fab staging build_cars_base)'
        exit()
    with cd(env.project_dir):
        virtualenv('python manage.py build_cars_base %s' % arg)


def resetdb():
    ''' this function will reset the entire database with new fixture '''
    if not env.hosts:
        print 'Error: must use enviroment (e.g fab staging resetdb)'
        exit()
    with cd(env.project_dir):
        virtualenv('python manage.py dba_init_db')


def deploy(resetdb=False):
    ''' deployment function '''
    if not env.hosts:
        print 'Error: must use enviroment (e.g fab staging deploy)'
        exit()

    if not exists(env.project_dir):
        print 'Error: the project directory does not exists.'
        exit()

    # install pip requirements
    now = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    with cd(env.project_dir):
        git_pull(env.git_merge_with)
        git_pull(env.git_branch)
        git('merge %s' % env.git_merge_with)
        git('tag %s' % now)
        git('push')
        if exists('garcom/misc/setting_templates/local_env.py'):
            run('rm garcom/misc/setting_templates/local_env.py')

        run('cp %(TEMPLATE_SETTING_DIR)s%(TEMPLATE_SETTING)s garcom/misc/setting_templates/local_env.py' %
            {'TEMPLATE_SETTING_DIR': env.config_template_dir,
             'TEMPLATE_SETTING': env.template_setting})

        virtualenv('pip install -r requirements.pip ')

        virtualenv('python manage.py syncdb --noinput')

        virtualenv('python manage.py collectstatic --noinput')

    restart_celery()
    restart_uwsgi()

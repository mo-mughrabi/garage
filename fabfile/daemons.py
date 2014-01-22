from fabric.api import sudo, env, cd
from misc import virtualenv


def restart_uwsgi():
    '''restart uwsgi through supervisord'''
    if not env.hosts:
        print 'Error: must use enviroment (e.g fab stagign deploy)'
        exit()
    sudo('supervisorctl restart %s' % env.uwsgi_instance)


def start_celerycam():
    '''Start celerycam daemon'''
    with cd(env.project_dir):
        virtualenv('python manage.py celerycam --logfile=%scelerycam.log --pidfile=%scelerycam.pid --detach' % (
        env.celery_log_dir, env.celery_log_dir))


def stop_celerycam():
    '''Stop celerycam daemon'''
    with cd(env.project_dir):
        virtualenv("kill `ps ax| grep -v awk| awk '/celerycam/{print $1}'`")


def restart_celerycam():
    stop_celerycam()
    start_celerycam()


def stop_celery():
    '''Stop celery daemon'''
    with cd(env.project_dir):
        virtualenv('python manage.py celeryd_multi stop celery --pidfile=%scelery.pid' % env.celery_log_dir)


def start_celery():
    '''Start celery daemon'''
    with cd(env.project_dir):
        virtualenv(
            'python manage.py celeryd_multi start celery -B -E --logfile=%scelery.log --pidfile=%scelery.pid --loglevel=INFO' % (
            env.celery_log_dir, env.celery_log_dir))


def restart_celery():
    '''Restart celery daemon'''
    with cd(env.project_dir):
        virtualenv(
            'python manage.py celeryd_multi restart celery -B -E --logfile=%scelery.log --pidfile=%scelery.pid --loglevel=INFO' % (
            env.celery_log_dir, env.celery_log_dir))


def force_kill_celery():
    '''Force kill celeryd processes (emergency only)'''
    cmd = '''ps aux |grep celery | grep -v grep | grep -v celerycam | awk '{print $2}' | xargs kill -9'''
    sudo(cmd)
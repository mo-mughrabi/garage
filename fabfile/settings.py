from fabric.api import env

env.roledefs = {
    'staging': ['IP_ADDRESS'],
    'production': ['IP_ADDRESS'],

}


def staging():
    """Set staging environment"""
    env.hosts = ['IP_ADDRESS', ]
    env.user = 'ubuntu'  # linux user
    env.warn_only = True
    env.no_keys = False
    env.key_filename = './fabfile/keys/staging.pem'

    env.virtualenv_dir = '/home/ubuntu/garenv/'
    env.project_dir = '%sgarage/' % env.virtualenv_dir
    env.config_template_dir = '%sgarcom/misc/setting_templates/' % env.project_dir
    env.template_setting = 'staging.py'
    env.git_branch = 'staging'
    env.git_merge_with = 'dev'
    env.name = 'staging site'
    env.uwsgi_instance = 'garage'

    env.celery_log_dir = '%slogs/' % env.virtualenv_dir


def production():
    """Set staging environment"""
    env.hosts = ['IP_ADDRESS', ]
    env.user = 'ubuntu'  # linux user
    env.warn_only = True
    env.no_keys = False
    env.key_filename = './fabfile/keys/gar-prod.pem'

    env.virtualenv_dir = '/home/ubuntu/garenv/'
    env.project_dir = '%sgarage/' % env.virtualenv_dir
    env.config_template_dir = '%sgarcom/misc/setting_templates/' % env.project_dir
    env.template_setting = 'production.py'
    env.git_branch = 'master'
    env.git_merge_with = 'staging'
    env.name = 'production site'
    env.uwsgi_instance = 'garage'

    env.celery_log_dir = '%slogs/' % env.virtualenv_dir
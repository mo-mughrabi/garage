from fabric.api import env, run
import os


def virtualenv(cmd, p_pty=True):
    '''Run command inside virtualenv'''
    run('. %s && %s' % (os.path.join(env.virtualenv_dir, 'bin', 'activate'), cmd), pty=p_pty)


def git(command):
    '''Run git command'''
    run('git %s' % command)


def git_pull(branch):
    '''Checkout a branch, and git pull'''
    git('checkout %s' % branch)
    git('pull')
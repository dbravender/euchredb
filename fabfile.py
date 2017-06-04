import os
from StringIO import StringIO

from fabric.api import task, local, run
from fabric.operations import put
from fabric.state import env

from gitric.api import (  # noqa
    git_seed, git_reset, allow_dirty, force_push,
    init_bluegreen, swap_bluegreen
)


@task
def prod():
    env.user = 'euchredb'
    env.bluegreen_root = '/home/euchredb/euchredb-bluegreen/'
    env.bluegreen_ports = {'blue': '8111',
                           'green': '8222'}
    init_bluegreen()


@task
def deploy(commit=None):
    if not commit:
        commit = local('git rev-parse HEAD', capture=True)
    env.repo_path = os.path.join(env.next_path, 'repo')
    git_seed(env.repo_path, commit)
    git_reset(env.repo_path, commit)
    run('kill $(cat %(pidfile)s) || true' % env)
    run('virtualenv %(virtualenv_path)s' % env)
    run('source %(virtualenv_path)s/bin/activate && '
        'pip install -r %(repo_path)s/requirements.txt'
        % env)
    put(StringIO('proxy_pass http://127.0.0.1:%(bluegreen_port)s/;' % env),
        env.nginx_conf)
    run('cd %(repo_path)s && PYTHONPATH=. '
        '%(virtualenv_path)s/bin/gunicorn -D '
        '-b 0.0.0.0:%(bluegreen_port)s -p %(pidfile)s app:app' % env)


@task
def cutover():
    swap_bluegreen()
    run('sudo /etc/init.d/nginx reload')

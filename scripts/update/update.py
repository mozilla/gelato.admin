"""
Deploy this project in dev/stage/production.

Requires commander_ which is installed on the systems that need it.

.. _commander: https://github.com/oremj/commander
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commander.deploy import task, hostgroups, BadReturnCode
import commander_settings as settings

@task
def create_virtualenv(ctx):
    venv = settings.VIRTUAL_ENV
    if not venv.startswith('/data'):
        raise Exception('venv must start with /data') # this is just to avoid rm'ing /

    ctx.local('rm -rf %s' % venv)
    ctx.local('virtualenv --distribute --never-download %s' % venv)

    ctx.local('%s/bin/pip install --exists-action=w --no-deps --no-index '
              '--download-cache=/tmp/pip-cache -f %s '
              '-r %s/requirements/prod.txt' %
              (venv, settings.PYREPO, settings.SRC_DIR))

    # make sure this always runs
    ctx.local("rm -f %s/lib/python2.6/no-global-site-packages.txt" % venv)
    ctx.local("%s/bin/python /usr/bin/virtualenv --relocatable %s" % (venv, venv))

@task
def update_code(ctx, tag):
    """Update the code to a specific git reference (tag/sha/etc)."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('git fetch')
        ctx.local('git reset --hard %s' % tag)

@task
def update_assets(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("%s manage.py collectstatic --noinput" % settings.PYTHON)


@task
def checkin_changes(ctx):
    """Use the local, IT-written deploy script to check in changes."""
    ctx.local(settings.DEPLOY_SCRIPT)


@hostgroups(settings.WEB_HOSTGROUP, remote_kwargs={'ssh_key': settings.SSH_KEY})
def deploy_app(ctx):
    """Call the remote update script to push changes to webheads."""
    ctx.remote(settings.REMOTE_UPDATE_SCRIPT)
    ctx.remote('service %s reload' % settings.GUNICORN)


@task
def update_info(ctx):
    """Write info about the current state to a publicly visible file."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('date')
        ctx.local('git branch')
        ctx.local('git log -3')
        ctx.local('git status')

@task
def pre_update(ctx, ref=settings.UPDATE_REF):
    """Update code to pick up changes to this file."""
    update_code(ref)
    update_info()


@task
def post_update(ctx):
    pass

@task
def update(ctx):
#    update_assets()
    pass


@task
def deploy(ctx):
    checkin_changes()
    deploy_app()


@task
def update_site(ctx, tag):
    """Update the app to prep for deployment."""
    pre_update(tag)
    create_virtualenv()
    update()
    post_update()

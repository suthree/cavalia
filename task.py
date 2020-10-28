#! /usr/bin/env python
import os
import shutil

from invoke import task, run

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
COOKIE = os.path.join(BASE_DIR, 'flask_app')
REQUIREMENTS = os.path.join.(BASE_DIR, 'requirements', 'dev.txt')


@task
def build():
    run('cookiecutter {0} --no-input'.format(BASE_DIR))


@task
def clean():
    if os.path.exists(COOKIE):
        shutil.rmtree(COOKIE)
        print('remove {0}'.format(COOKIE))
    else:
        print('app diretory does not exist. skipping')


@task
def test():
    run('pip install -r {0}'.format(REQUIREMENTS), echo=True)
    run('python {0} test'.format(os.path.join(COOKIE, 'manage.py')), echo=True)
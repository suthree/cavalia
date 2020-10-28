from flask import render_template, Response
from flask_login import login_required

from . import user


@user.route('/user')
# @login_required
def login():
    return Response('hello world')
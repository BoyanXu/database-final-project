#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from functools import wraps
from flask import Flask, render_template, request, session, url_for, redirect
from flask.globals import current_app, session
from flask.helpers import flash, url_for

import pymysql
import pymysql.cursors

from appconf import app, conn

import register

import logging
from logging import Formatter, FileHandler
from forms import *
import os

# Login required decorator.

# def login_required(test):
#     @wraps(test)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return test(*args, **kwargs)
#         else:
#             flash('You need to login first.')
#             return redirect(url_for('login'))
#     return wrap


conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='', # password for XMAPP
                       db='university',
                       # port=5000,
                       unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

#Login page
@app.route('/login', methods=['GET'])
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)

#Login Authentication
@app.route('/login/auth', methods=['GET', 'POST'])
def loginAuth():
    form = LoginForm(request.form)
    print(form.name)
    return render_template('pages/placeholder.home.html')

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
    app.run(host='127.0.0.1', port=5000, debug = True)

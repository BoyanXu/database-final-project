from forms import *
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appconf import app, conn

#Login page
@app.route('/login', methods=['GET'])
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


#Login Authentication
@app.route('/login/auth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']
    usrtype  = request.form['usrtype']
    if True:
        form = LoginForm(request.form)
        errorString = "Username or password is incorrect"
        return render_template('forms/login.html', form=form, error=errorString)

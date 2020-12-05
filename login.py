from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appconf import app, conn
from forms import *

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

    if usrtype == 'customer':
        query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    elif usrtype == 'agent':
        query = 'SELECT * FROM booking_agent WHERE email = %s and password = md5(%s)'
    else:
        query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'

    cursor = conn.cursor()
    cursor.execute(query, (username, password))

    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username # Use primary-key
        if usrtype == 'staff':
            return redirect(url_for('staffHome'))
        elif usrtype == 'customer':
            return redirect(url_for('customerHome'))
        else:
            return redirect(url_for('agentHome'))
    else:
        form = LoginForm(request.form)
        errorString = "Username or password is incorrect"
        return render_template('forms/login.html', form=form, error=errorString)

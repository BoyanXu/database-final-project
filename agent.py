from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime

from appconf import app, conn
from forms import *

@app.route('/agentHome')
def agentHome():
    username = session['username']

    cursor = conn.cursor()
    query = """
        """
    cursor.execute(query, (XXX))
    data = cursor.fetchall()
    cursor.close()

    return render_template("pages/agentHome.html", username=username, data=data)
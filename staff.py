from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime

from appconf import app, conn
from forms import *


def getAirlineName(username):
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    return data['airline_name']


@app.route('/staffHome')
def staffHome():
    username = session['username']
    airlineName = getAirlineName(username)

    cursor = conn.cursor()
    query = """SELECT * FROM flight
                WHERE  airline_name = %s
                    AND (
                        ( departure_time BETWEEN Curdate() AND Date_add(Curdate(), interval 30 day) )
                        OR
                        ( arrival_time BETWEEN Curdate() AND Date_add(Curdate(), interval 30 day) )
                        )
        """
    cursor.execute(query, (airlineName))
    data = cursor.fetchall()
    cursor.close()
    return render_template("pages/staffHome.html", username=username, data=data)
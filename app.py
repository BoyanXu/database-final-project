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

# route modules
import register
import login
import customer
import agent
import staff

import logging
from logging import Formatter, FileHandler
from forms import *
import os

conn = pymysql.connect(host='127.0.0.1',
                       user='root',
                       password='', # password for XMAPP
                       db='airline_service_db',
                       # port=5000,
                       unix_socket='/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/search', methods=['GET'])
def publicSearch():
    form = FlightSearchForm(request.form)
    return render_template('pages/publicSearch.html', form=form)

@app.route('/search/result', methods=['GET', 'POST'])
def publicSearchResult():
    fromCity = request.form['fromCity']
    fromAirport = request.form['fromAirport']
    fromDate = request.form['fromDate']
    toCity = request.form['toCity']
    toAirport = request.form['toAirport']
    toDate = request.form['toDate']
    query = """SELECT distinct f.airline_name,
                f.flight_num,
                departure_airport,
                departure_time,
                arrival_airport,
                arrival_time,
                price,
                airplane_id
                    FROM flight as f, airport
                    WHERE airport.airport_name=f.departure_airport
                    AND airport.airport_city = %s
                    AND airport.airport_name = %s
                    AND %s BETWEEN DATE_SUB(f.departure_time, INTERVAL 2 DAY) AND DATE_ADD(f.departure_time, INTERVAL 2 DAY)
                    AND %s BETWEEN DATE_SUB(f.arrival_time, INTERVAL 2 DAY) AND DATE_ADD(f.arrival_time, INTERVAL 2 DAY)
                    AND (f.airline_name, f.flight_num) in
                        (SELECT flight.airline_name, flight.flight_num FROM flight, airport
                            WHERE airport.airport_name=flight.arrival_airport
                            AND airport.airport_city = %s
                            AND airport.airport_name = %s)
                    AND (SELECT DISTINCT seats FROM flight, airplane
                            WHERE flight.airplane_id = airplane.airplane_id
                            AND flight.airline_name = airplane.airline_name
                            AND flight.airline_name = f.airline_name
                            AND flight.flight_num = f.flight_num) >=
                                (SELECT COUNT(*) FROM ticket
                                    WHERE ticket.airline_name = f.airline_name
                                    AND ticket.flight_num = f.flight_num)
    """

    cursor = conn.cursor()
    cursor.execute(query, (fromCity, fromAirport, fromDate, toDate, toCity, toAirport))
    data = cursor.fetchall()
    cursor.close()

    if(data):
        form = FlightSearchForm(request.form)
        return render_template('pages/publicSearch.html', form=form, results=data)
    else:
        form = FlightSearchForm(request.form)
        error = 'No results found'
        return render_template('pages/publicSearch.html', form=form, error=error)

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/login')


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.
@app.route('/index')
def index():
    return render_template('pages/placeholder.index.html')

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
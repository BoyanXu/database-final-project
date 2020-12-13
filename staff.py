from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime

from appconf import app, conn, validateDates
from forms import *

from datetime import date, timedelta

def today():
    return date.today().isoformat()

def last1mon():
    return (date.today() - timedelta(days=30)).isoformat()

def last6mons():
    return (date.today() - timedelta(days=180)).isoformat()

def last1year():
    return (date.today() - timedelta(days=365)).isoformat()

def getReport(username, fromDate=last6mons(), toDate=today()):
    fromDate=last6mons()
    toDate=today()
    cursor = conn.cursor()
    query = """SELECT YEAR(purchase_date) as year, MONTH(purchase_date) as month, COUNT(ticket_id) as sales
                FROM purchases NATURAL JOIN ticket JOIN flight USING(airline_name, flight_num)
                    WHERE  airline_name = %s
                    AND purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                GROUP BY year, month"""
    cursor.execute(query, (username, fromDate, toDate))
    data = cursor.fetchall()
    cursor.close()

    labels = []
    dataset = []

    for line in data:
        label = str(line['year']) + '-'  + str(line['month'])
        data  = int(line['sales'])
        labels.append(label)
        dataset.append(data)
    return labels, dataset

def getStaffAirline(username):
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airline_staff WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    return data['airline_name']

def getTopDestinations(airline):
    cursor = conn.cursor()
    query = """SELECT airport_city, COUNT(ticket_id) as count FROM airport, ticket JOIN flight USING(airline_name, flight_num)
                    WHERE airport_name = arrival_airport
                    AND airline_name=%s GROUP by airport_city ORDER by count DESC LIMIT 3
            """
    cursor.execute(query, (airline))
    data = cursor.fetchall()
    cursor.close()
    return data # Purchase dates

def getReport(airline, fromDate=last6mons(), toDate=today()):
    cursor = conn.cursor()
    query = """SELECT YEAR(purchase_date) as year, MONTH(purchase_date) as month, COUNT(ticket_id) as sales
                FROM purchases NATURAL JOIN ticket JOIN flight USING(airline_name, flight_num)
                    WHERE  airline_name = %s
                    AND purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                GROUP BY year, month
            """
    cursor.execute(query, (airline, fromDate, toDate))
    data = cursor.fetchall()
    cursor.close()
    return data

def getRevenue(airline):
    query = """SELECT *  FROM
                (SELECT SUM(price) as unagented FROM purchases NATURAL JOIN ticket JOIN flight USING(airline_name, flight_num)
                    WHERE  airline_name = %s
                    AND purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                    AND booking_agent_id IS NULL) as a,
                (SELECT SUM(price) as agented FROM purchases NATURAL JOIN ticket JOIN flight USING(airline_name, flight_num)
                    WHERE  airline_name = %s
                    AND purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                    AND booking_agent_id IS NOT NULL) as b
    """
    cursor = conn.cursor()
    cursor.execute(query, (airline, last1mon(), today(), airline, last1mon(), today()))
    last1MonData = cursor.fetchone()
    cursor.execute(query, (airline, last1year(), today(), airline, last1year(), today()))
    last1YearData = cursor.fetchone()
    cursor.close()
    return last1MonData, last1YearData


def authorizeStaffSession():
    username = session['username']
    query = 'SELECT * from airline_staff WHERE username=%s'
    cursor = conn.cursor()
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()
    if data:
        return True
    else:
        session.pop('username')
        return False


@app.route('/staffHome', methods=["GET", "POST"])
def staffHome():
    username = session['username']
    airlineName = getStaffAirline(username)

    if request.method == "POST":
        flight_num = request.form['flight_num']
        status = request.form['status']
        cursor = conn.cursor()
        query = """UPDATE flight SET status=%s
                    WHERE flight_num=%s AND airline_name = %s
            """
        cursor.execute(query, (status, flight_num, airlineName))
        conn.commit()
        cursor.close()

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

    topDestinations = getTopDestinations(airlineName)

    last1MonData, last1YearData = getRevenue(airlineName)

    last1Monlabels = ['agented', 'unagented']
    last1Mondataset = [int(last1MonData['agented']), int(last1MonData['unagented'])]

    last1Yearlabels = ['agented', 'unagented']
    last1Yeardataset = [int(last1YearData['agented']), int(last1YearData['unagented'])]

    form = ChangeFlightForm(request.form)
    return render_template("pages/staffHome.html", username=username, data=data,
                           last1Monlabels   = last1Monlabels,
                           last1Mondataset  = last1Mondataset,
                           last1Yearlabels  = last1Yearlabels,
                           last1Yeardataset = last1Yeardataset,
                           form             = form,
                           topDestinations  = topDestinations)


@app.route("/staffHome/createFlight", methods=["GET"])
def staffCreateFlight():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]
    form = CreateFlightForm(request.form)
    return render_template("pages/staffCreateFlight.html", username=username, form=form)

@app.route("/staffHome/createFlight/status", methods=["GET", "POST"])
def staffCreateFlightStatus():
    if not authorizeStaffSession():
        return redirect(url_for('index'))

    username     = session["username"]
    airline      = getStaffAirline(username)
    flightNumber = request.form['flightNumber']
    fromAirport  = request.form['fromAirport']
    fromDateTime = request.form['fromDateTime']
    toAirport    = request.form['toAirport']
    toDateTime   = request.form['toDateTime']
    price        = request.form['price']
    status       = 'Upcoming'
    airplane_id  = request.form['airplane_id']

    if not validateDates(fromDateTime, toDateTime):
        form  = CreateFlightForm(request.form)
        return render_template("pages/staffCreateFlight.html", username=username, form=form, error="Invalid Time Interval")

    cursor = conn.cursor()
    query = """
            INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    cursor.execute(query, (airline, flightNumber, fromAirport, fromDateTime, toAirport, toDateTime, price, status, airplane_id))

    data = cursor.fetchone()
    conn.commit()
    cursor.close()

    form  = CreateFlightForm(request.form)
    return render_template("pages/staffCreateFlight.html", username=username, form=form, success="Flight Inserted successfully")

@app.route("/staffHome/createAirplane", methods=["GET"])
def staffCreateAirplane():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]
    form = CreateAirplaneForm(request.form)
    return render_template("pages/staffCreateAirplane.html", username=username, form=form)

@app.route("/staffHome/createAirplane/status", methods=["GET", "POST"])
def staffCreateAirplaneStatus():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]

    airline = getStaffAirline(username)
    airplane_id = request.form['airplane_id']
    seats = request.form['seats']

    cursor = conn.cursor()
    query = """
            INSERT INTO airplane VALUES(%s, %s, %s)  """
    cursor.execute(query, (airline, airplane_id, seats))

    data = cursor.fetchone()
    conn.commit()
    cursor.close()
    form = CreateAirplaneForm(request.form)
    # TODO Handle airplane duplication
    return render_template("pages/staffCreateAirplane.html", username=username, form=form, success="Airplane Inserted successfully")

@app.route("/staffHome/createAirport", methods=["GET"])
def staffCreateAirport():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]
    form = CreateAirportForm(request.form)
    return render_template("pages/staffCreateAirport.html", username=username, form=form)

@app.route("/staffHome/createAirport/status", methods=["GET", "POST"])
def staffCreateAirportStatus():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]
    name = request.form['name']
    city = request.form['city']

    cursor = conn.cursor()
    query = """
            INSERT INTO airport VALUES (%s, %s) """
    cursor.execute(query, (name, city))
    conn.commit()
    cursor.close()

    form = CreateAirportForm(request.form)
    return render_template("pages/staffCreateAirport.html", username=username, form=form, success="Airport Inserted successfully")

@app.route("/staffHome/viewAgent", methods=["GET"])
def staffViewAgent():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]
    form     = ViewAgentForm(request.form)
    return render_template("pages/staffViewAgent.html", username=username, form=form)

@app.route("/staffHome/viewAgent/status", methods=["GET", "POST"])
def staffViewAgentStatus():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]
    airline  = getStaffAirline(username)
    range    = request.form['range']
    criteria = request.form['criteria']
    cursor = conn.cursor()

    query = ""
    if criteria == "sale" and range == "year":
        query ="""SELECT email, COUNT(ticket_id) as sale
                    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                    JOIN flight USING(airline_name, flight_num)
                        WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
                        AND airline_name=%s GROUP BY email ORDER BY sale DESC LIMIT 5
                """
    elif criteria == "sale" and range == "month":
        query ="""SELECT email, COUNT(ticket_id) as sale
                    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                    JOIN flight USING(airline_name, flight_num)
                        WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 MONTH)
                        AND airline_name=%s GROUP BY email ORDER BY sale DESC LIMIT 5
                """
    elif criteria == "commission" and range == "year":
        query = """SELECT email, SUM(price) as commission
                    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                    JOIN flight USING(airline_name, flight_num)
                        WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
                        AND airline_name=%s GROUP by email ORDER by commission DESC LIMIT 5
                """
    elif criteria == "commission" and range == "month":
        query ="""SELECT email, SUM(price) as commission
                    FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                    JOIN flight USING(airline_name, flight_num)
                        WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 MONTH)
                        AND airline_name=%s GROUP by email ORDER by commission DESC LIMIT 5
                """
    cursor.execute(query, (airline))
    data = cursor.fetchall()
    cursor.close()

    form = ViewAgentForm(request.form)
    return render_template("pages/staffViewAgent.html", username=username, form=form, criteria=criteria, data=data)


@app.route("/staffHome/viewReport", methods=["GET", "POST"])
def staffViewReport():
    if not authorizeStaffSession():
        return redirect(url_for('index'))
    username = session["username"]
    airline  = getStaffAirline(username)

    if request.method == "POST":
        data = getReport(airline, request.form['fromDate'], request.form['toDate'])
    else:
        data = getReport(airline)

    labels = []
    dataset = []
    for line in data:
        label = str(line['year']) + '-'  + str(line['month'])
        data  = int(line['sales'])
        labels.append(label)
        dataset.append(data)

    form = StaffReportForm(request.form)
    return render_template("pages/staffViewReport.html", username=username, form=form, labels=labels, dataset=dataset)

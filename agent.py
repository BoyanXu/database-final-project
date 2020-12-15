from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime

from appconf import app, conn
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

def getAgentID(username):
    cursor = conn.cursor()
    query = 'SELECT booking_agent_id FROM booking_agent WHERE email=%s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    return data['booking_agent_id']

def getCommission(username, fromDate=last1mon(), toDate=today()):
    cursor = conn.cursor()
    query = """SELECT SUM(price) as commission
                FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                JOIN flight USING(airline_name, flight_num)
                    WHERE purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                    AND email=%s GROUP by email
            """
    cursor.execute(query, (fromDate, toDate, username))
    data = cursor.fetchone()
    cursor.close()
    try:
        return data['commission']
    except:
        return "Null"

def getSales(username, fromDate=last1mon(), toDate=today()):
    cursor = conn.cursor()
    query = """SELECT COUNT(*) as sales
                FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                JOIN flight USING(airline_name, flight_num)
                    WHERE purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                    AND email=%s GROUP by email
            """
    cursor.execute(query, (fromDate, toDate, username))
    data = cursor.fetchone()
    cursor.close()
    try:
        return data['sales']
    except:
        return "Null"

@app.route('/agentHome', methods=['GET', 'POST'])
def agentHome():
    username = session['username']
    if request.method == 'GET':
        commission = getCommission(username)
        sales      = getSales(username)
    else:
        commission = getCommission(username, request.form['fromDate'], request.form['toDate'])
        sales = getSales(username, request.form['fromDate'], request.form['toDate'])

    cursor = conn.cursor()
    query = """
            SELECT ticket.ticket_id, ticket.airline_name, ticket.flight_num,
                departure_airport, departure_time, arrival_airport, arrival_time, airplane_id, status,
                price, customer_email, purchases.booking_agent_id, purchase_date
                    FROM purchases, ticket, flight, booking_agent
                    WHERE purchases.ticket_id = ticket.ticket_id
                        AND ticket.airline_name = flight.airline_name
                        AND ticket.flight_num   = flight.flight_num
                        AND booking_agent.email = %s
                        AND booking_agent.booking_agent_id = purchases.booking_agent_id
                        AND departure_time > curdate() ORDER BY customer_email"""
    cursor.execute(query, (username))
    flightData = cursor.fetchall()
    cursor.close()
    form = AgentSaleForm(request.form)
    return render_template("pages/agentHome.html", username=username, form=form, flightData=flightData, commission=commission, sales=sales)

@app.route("/agentHome/purchase", methods=["GET"])
def agentPurchase():
    username = session["username"]
    form = AgentPurchaseForm(request.form)
    return render_template('pages/agentPurchase.html', username=username, form=form)

@app.route("/agentHome/purchase/status", methods=["GET", "POST"])
def agentPurchaseStatus():
    username = session["username"]
    airlineName = request.form['airlineName']
    flightNumber = request.form['flightNumber']
    customerEmail = request.form['customerEmail']

    cursor = conn.cursor()
    query = """
            SELECT MAX(ticket_id) + 1 as nxt_ticket_id FROM ticket
                WHERE (SELECT COUNT(*) as count FROM ticket
                        WHERE ticket.airline_name = %s AND ticket.flight_num = %s
                    ) < (SELECT airplane.seats as seats FROM flight, airplane
                            WHERE flight.airline_name = %s AND flight.flight_num = %s
                            AND flight.airplane_id = airplane.airplane_id)
            """
    cursor.execute(query, (airlineName, flightNumber, airlineName, flightNumber))
    data = cursor.fetchone()

    if data['nxt_ticket_id'] is None:
        cursor.close()
        error = "Purchase Failed, make sure you typed the name correctly and the flight has enough seat"
        form  = AgentPurchaseForm(request.form)
        return render_template('pages/customerPurchase.html', username=username, form=form, error=error)
    else:
        nxt_ticket_id = data['nxt_ticket_id']
        queryInsertTicket = """
                            INSERT INTO ticket VALUES(%s, %s, %s)
                            """
        cursor.execute(queryInsertTicket, (nxt_ticket_id, airlineName, flightNumber))
        queryInsertPurchase ="""
                                INSERT INTO purchases VALUES(%s, %s, %s, CURDATE())
                                """
        cursor.execute(queryInsertPurchase, (nxt_ticket_id, customerEmail, getAgentID(username)))
        data = cursor.fetchone()
        conn.commit()
        cursor.close()

        form  = AgentPurchaseForm(request.form)
        return render_template('pages/agentPurchase.html', username=username, form=form, results=data, myTicket=nxt_ticket_id)


@app.route("/agentHome/viewCustomer", methods=["GET"])
def agentViewCustomer():
    username = session["username"]
    form     = ViewCustomerForm(request.form)
    return render_template("pages/agentViewCustomer.html", username=username, form=form)


@app.route("/agentHome/viewCustomer/status", methods=["GET", "POST"])
def agentViewCustomerStatus():
    username = session["username"]
    range    = request.form['range']
    criteria = request.form['criteria']
    cursor = conn.cursor()

    query = ""
    if criteria == "sale" and range == "year":
        query ="""  SELECT customer_email, COUNT(ticket_id) as sale
                        FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                        JOIN flight USING(airline_name, flight_num)
                        WHERE booking_agent.email = %s
                        AND purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
                        GROUP BY customer_email ORDER BY sale DESC LIMIT 5
                """
    elif criteria == "sale" and range == "month":
        query ="""SELECT customer_email, COUNT(ticket_id) as sale
                        FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                        JOIN flight USING(airline_name, flight_num)
                        WHERE booking_agent.email = %s
                        AND purchase_date >= date_sub(curdate(), INTERVAL 6 MONTH)
                            GROUP BY customer_email ORDER BY sale DESC LIMIT 5
                """
    elif criteria == "commission" and range == "year":
        query = """  SELECT customer_email, SUM(price) as commission
                        FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                        JOIN flight USING(airline_name, flight_num)
                        WHERE booking_agent.email = %s
                        AND purchase_date >= date_sub(curdate(), INTERVAL 1 YEAR)
                            GROUP by customer_email ORDER by commission DESC LIMIT 5
                """
    elif criteria == "commission" and range == "month":
        query =""" SELECT customer_email, SUM(price) as commission
                        FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                        JOIN flight USING(airline_name, flight_num)
                        WHERE booking_agent.email = %s
                        AND purchase_date >= date_sub(curdate(), INTERVAL 6 MONTH)
                            GROUP by customer_email ORDER by commission DESC LIMIT 5
                """
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()

    labels = []
    dataset = []

    for line in data:
        label = line['customer_email']
        sales  = line[criteria]
        labels.append(label)
        dataset.append(int(sales))

    form = ViewCustomerForm(request.form)
    return render_template("pages/agentViewCustomer.html", username=username, form=form, criteria=criteria, data=data, labels=labels, dataset=dataset)

@app.route('/agentHome/search', methods=['GET'])
def agentSearch():
    username = session["username"]
    form = FlightSearchForm(request.form)
    return render_template('pages/agentSearch.html', username=username, form=form)


@app.route('/agentHome/search/results', methods=['GET', 'POST'])
def agentSearchHandler():

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
                    AND f.departure_time BETWEEN DATE_SUB(%s, INTERVAL 2 DAY) AND DATE_ADD(%s, INTERVAL 2 DAY)
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
        username = session["username"]
        form = FlightSearchForm(request.form)
        return render_template('pages/agentSearch.html', username=username, form=form, results=data)
    else:
        #returns an error message to the html page
        username = session["username"]
        form = FlightSearchForm(request.form)
        error = 'No results found'
        return render_template('pages/agentSearch.html', username=username, form=form, error=error)
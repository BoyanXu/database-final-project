from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appconf import app, conn
from forms import *
from charts import *

from datetime import date, timedelta

def today():
    return date.today().isoformat()

def last6mons():
    return (date.today() - timedelta(days=180)).isoformat()

def getSpending(username, fromDate=last6mons(), toDate=today()):
    cursor = conn.cursor()
    # default track last 6 month
    query = """SELECT SUM(flight.price) as TotalSpending
                FROM purchases, ticket, flight
                    WHERE purchases.customer_email = %s
                    AND purchases.ticket_id = ticket.ticket_id
                    AND ticket.airline_name = flight.airline_name
                    AND ticket.flight_num = flight.flight_num
                    AND purchases.purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                    GROUP BY purchases.customer_email"""
    cursor.execute(query, (username, fromDate, toDate))
    data = cursor.fetchone()
    cursor.close()
    try:
        return data['TotalSpending']
    except:
        return "Null"


def getSpendingDistr(username):
    fromDate=last6mons()
    toDate=today()
    cursor = conn.cursor()
    query = """SELECT SUM(flight.price) as spend, YEAR(purchases.purchase_date) as year, MONTH(purchases.purchase_date) as month
                    FROM purchases, ticket, flight
                    WHERE purchases.customer_email = %s
                        AND purchases.ticket_id = ticket.ticket_id
                        AND ticket.airline_name = flight.airline_name
                        AND ticket.flight_num = flight.flight_num
                        AND purchases.purchase_date BETWEEN date_sub(%s, INTERVAL 2 DAY) AND date_sub(%s, INTERVAL 2 DAY)
                    GROUP BY year, month
                    ORDER BY purchases.purchase_date"""
    cursor.execute(query, (username, fromDate, toDate))
    data = cursor.fetchall()
    cursor.close()

    labels = []
    dataset = []

    for line in data:
        label = str(line['year']) + '-'  + str(line['month'])
        data  = int(line['spend'])
        labels.append(label)
        dataset.append(data)
    return labels, dataset


@app.route("/customerHome", methods=["GET", "POST"])
def customerHome():
    username = session["username"]

    query = """
                SELECT purchases.ticket_id,
                    ticket.airline_name,
                    ticket.flight_num,
                    flight.departure_airport,
                    flight.departure_time,
                    flight.arrival_airport,
                    flight.arrival_time,
                    flight.price,
                    flight.status,
                    flight.airplane_id
                FROM purchases, ticket, flight
                        WHERE purchases.customer_email = %s
                        AND purchases.ticket_id = ticket.ticket_id
                        AND ticket.airline_name = flight.airline_name
                        AND ticket.flight_num = flight.flight_num
                        AND departure_time > curdate();
    """

    cursor = conn.cursor()
    cursor.execute(query, (username))
    data = cursor.fetchall()
    cursor.close()

    if request.method == "POST":
        fromDate = request.form['fromDate']
        toDate   = request.form['toDate']
        mySpending = getSpending(username, fromDate, toDate)
    else:
        mySpending = getSpending(username)

    labels, dataset = getSpendingDistr(username)

    form = TrackSpendingForm(request.form)
    return render_template("pages/customerHome.html", username=username, posts=data, form=form, mySpending=mySpending, labels=labels, dataset=dataset)


@app.route("/customerHome/purchase", methods=["GET"])
def customerPurchase():
    username = session["username"]
    form = PurchaseForm(request.form)
    return render_template('pages/customerPurchase.html', username=username, form=form)

@app.route("/customerHome/purchase/status", methods=["GET", "POST"])
def customerPurchaseStatus():
    username = session["username"]
    airlineName = request.form['airlineName']
    flightNumber = request.form['flightNumber']

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
        form  = PurchaseForm(request.form)
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
        cursor.execute(queryInsertPurchase, (nxt_ticket_id, username, None))
        data = cursor.fetchone()
        conn.commit()
        cursor.close()

        form  = PurchaseForm(request.form)
        return render_template('pages/customerPurchase.html', username=username, form=form, results=data, myTicket=nxt_ticket_id)


@app.route('/customerHome/search', methods=['GET'])
def customerSearch():
    username = session["username"]
    form = FlightSearchForm(request.form)
    return render_template('pages/customerSearch.html', username=username, form=form)


@app.route('/customerHome/search/results', methods=['GET', 'POST'])
def customerSearchHandler():

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
        return render_template('pages/customerSearch.html', username=username, form=form, results=data)
    else:
        #returns an error message to the html page
        username = session["username"]
        form = FlightSearchForm(request.form)
        error = 'No results found'
        return render_template('pages/customerSearch.html', username=username, form=form, error=error)
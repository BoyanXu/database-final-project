from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime

from appconf import app, conn
from forms import *

def getAgentID(username):
    cursor = conn.cursor()
    query = 'SELECT booking_agent_id FROM booking_agent WHERE email=%s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    return data['booking_agent_id']

def getCommission(username):
    cursor = conn.cursor()
    query = """SELECT SUM(price) as commission
                FROM booking_agent NATURAL JOIN purchases NATURAL JOIN ticket
                JOIN flight USING(airline_name, flight_num)
                    WHERE purchase_date >= date_sub(curdate(), INTERVAL 1 MONTH)
                    AND email=%s GROUP by email
            """
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    try:
        return data['commission']
    except:
        return "Null"

@app.route('/agentHome', methods=['GET', 'POST'])
def agentHome():
    username = session['username']
    commission=getCommission(username)

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

    return render_template("pages/agentHome.html", username=username, flightData=flightData, commission=commission)

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



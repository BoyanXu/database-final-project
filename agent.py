from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime

from appconf import app, conn
from forms import *

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
    return data['commission']

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
from forms import *
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

from appconf import app, conn

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)

@app.route('/register/customer')
def registerCustomer():
    form = RegisterCustomerForm(request.form)
    return render_template('forms/registerCustomer.html', form=form)

@app.route('/register/agent')
def registerAgent():
    form = RegisterAgentForm(request.form)
    return render_template('forms/registerAgent.html', form=form)

@app.route('/register/staff')
def registerStaff():
    form = RegisterStaffForm(request.form)
    return render_template('forms/registerStaff.html', form=form)


@app.route('/register/customer/auth', methods=['POST'])
def registerCustomerAuth():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    building_number = request.form['buildingNumber']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone_number = request.form['phone']
    passport_number = request.form['passportNum']
    passport_expiration = request.form['passportExpiry']
    passport_country = request.form['passportCountry']
    date_of_birth = request.form['birth']

    cursor = conn.cursor()
    query = """INSERT INTO customer (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`)
                VALUES (%s, %s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    cursor.execute(query, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
    conn.commit()
    cursor.close()
    return redirect('/login')

@app.route('/register/agent/auth', methods=['POST'])
def registerAgentAuth():
    email = request.form['email']
    password = request.form['password']
    booking_agent_id = request.form['booking_agent_id']

    cursor = conn.cursor()
    query = """INSERT INTO booking_agent (`email`, `password`, `booking_agent_id`) VALUES (%s, md5(%s), %s)
            """
    cursor.execute(query, (email, password, booking_agent_id))
    conn.commit()
    cursor.close()
    return redirect('/login')

@app.route('/register/staff/auth', methods=['POST'])
def registerStaffAuth():
    username = request.form['username']
    password = request.form['password']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    date_of_birth = request.form['birth']
    airline_name = request.form['airline']

    cursor = conn.cursor()
    query = """INSERT INTO airline_staff (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`)
                VALUES (%s, md5(%s), %s, %s, %s, %s)
            """
    cursor.execute(query, (username, password, firstName, lastName, date_of_birth, airline_name))
    conn.commit()
    cursor.close()
    return redirect('/login')
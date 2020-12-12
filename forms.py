from flask_wtf import Form
from wtforms import TextField, PasswordField, IntegerField, SelectField
from wtforms.fields.html5 import DateField, DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )

class RegisterCustomerForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(max=50)]
    )
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    buildingNumber = TextField(
        'Building Number', validators=[DataRequired()]
    )
    street = TextField(
        'Street', validators=[DataRequired(), Length(max=30)]
    )
    city = TextField(
        'City', validators=[DataRequired()]
    )
    state = TextField(
        'State', validators=[DataRequired()]
    )
    phone = IntegerField(
        'Phone Number', validators=[DataRequired(), Length(max=11)]
    )
    passportNum = TextField(
        'Passport Number', validators=[DataRequired()]
    )
    passportExpiry = DateField(
        'Passport Expiration', validators=[DataRequired()], format = '%Y-%m-%d'
    )
    passportCountry = TextField(
        'Passport Country', validators=[DataRequired()]
    )
    birth = DateField(
        'Birthday', validators=[DataRequired()], format = '%Y-%m-%d'
    )

class RegisterAgentForm(Form):
    email            = TextField('Email', validators=[DataRequired(), Length(max=40)])
    password         = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
    confirm          = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    booking_agent_id = IntegerField('Booking Agent ID', validators=[DataRequired(), Length(max=11)])

class RegisterStaffForm(Form):
    username  = TextField('Username', validators=[DataRequired(), Length(max=25)])
    email     = TextField('Email', validators=[DataRequired(), Length(max=40)])
    password  = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
    confirm   = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    firstName = TextField('First Name', validators=[DataRequired()])
    lastName  = TextField('Last Name', validators=[DataRequired()])
    birth     = DateField('Birthday', validators=[DataRequired()], format = '%Y-%m-%d')
    airline   = TextField('Airline Name', validators=[DataRequired()])

class LoginForm(Form):
    username = TextField('Email or Username(staff only)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    usrtype  = SelectField('User Type', choices=[('customer', 'Customer'), ('agent', 'Booking Agent'), ('staff', 'Staff')], validators=[DataRequired()])


class ForgotForm(Form):
    email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])

class PurchaseForm(Form):
    airlineName  = TextField("Airline Name", validators=[DataRequired()])
    flightNumber = TextField("Flight Number", validators=[DataRequired()])

class FlightSearchForm(Form):
    fromCity    = TextField("From City", validators=[DataRequired()])
    fromAirport = TextField("From Airport", validators=[DataRequired()])
    fromDate    = DateField("From Date", validators=[DataRequired()])
    toCity      = TextField("To City", validators=[DataRequired()])
    toAirport   = TextField("To Airport", validators=[DataRequired()])
    toDate      = DateField("To Date", validators=[DataRequired()])

class TrackSpendingForm(Form):
    fromDate    = DateField("From Date", validators=[DataRequired()])
    toDate      = DateField("To Date", validators=[DataRequired()])

class ChangeFlightForm(Form):
    flight_num = TextField("Flight Number", validators=[DataRequired()])
    status     = SelectField('New Status', choices=[('Upcoming', 'Upcoming'), ('In-progress', 'In Progress'), ('Delayed', 'Delayed')], validators=[DataRequired()])

class CreateFlightForm(Form):
    # airlineName  = TextField("Airline Name", validators=[DataRequired()])  <- use getAirlineName() instead of input it
    flightNumber = TextField("Flight Number", validators=[DataRequired()])
    fromAirport  = TextField("From Airport", validators=[DataRequired()])
    fromDateTime = DateTimeLocalField("From Date Time", validators=[DataRequired()])
    toAirport    = TextField("To Airport", validators=[DataRequired()])
    toDateTime   = DateTimeLocalField("To Date Time", validators=[DataRequired()])
    price        = TextField("Price", validators=[DataRequired()]) # <- Integer check
    airplane_id  = TextField("Airplane ID", validators=[DataRequired()])

class CreateAirplaneForm(Form):
    airplane_id = TextField("Airplane ID", validators=[DataRequired()])
    seats       = TextField("Seats Capacity", validators=[DataRequired()])

class CreateAirportForm(Form):
    name = TextField("Airport Name", validators=[DataRequired()])
    city = TextField("Airport City", validators=[DataRequired()])

class ViewStaffForm(Form):
    range    = SelectField('Time Range', choices=[('month', 'Past Month'), ('year', 'Past Year')], validators=[DataRequired()])
    criteria = SelectField('Ranking Criteria', choices=[('sale', 'Ticket sales'), ('commission', 'Amount of commission')], validators=[DataRequired()])
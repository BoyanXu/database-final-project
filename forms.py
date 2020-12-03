from flask_wtf import Form
from wtforms import TextField, PasswordField, IntegerField
from wtforms.fields.html5 import DateField
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
    email = TextField(
        'Email', validators=[DataRequired(), Length(max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(max=50)]
    )
    confirm = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    booking_agent_id = IntegerField(
        'Booking Agent ID', validators=[DataRequired(), Length(max=11)]
    )

class RegisterStaffForm(Form):
    username = TextField(
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
    firstName = TextField(
        'First Name', validators=[DataRequired()]
    )
    lastName = TextField(
        'Last Name', validators=[DataRequired()]
    )
    birth = DateField(
        'Birthday', validators=[DataRequired()], format = '%Y-%m-%d'
    )
    airline = TextField(
        'Airline Name', validators=[DataRequired()]
    )

class LoginForm(Form):
    name = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

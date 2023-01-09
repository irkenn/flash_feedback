from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, EmailField
from wtforms.validators import InputRequired, NumberRange, URL, Optional, Length

class AddUserForm(FlaskForm):
    """Form for registering new users"""

    username = StringField('Username', validators=[InputRequired(message="Username cannot be blank"), Length(max=20, message="Provide a username of less than 20 characters")])
    password = PasswordField('Password', validators=[InputRequired(message="Password cannot be blank")])
    email = EmailField('Email', validators=[InputRequired(message="Email cannot be blank"), Length(max=50, message="Provide an email of less than 50 characters")])
    first_name = StringField('First name', validators=[InputRequired(message="Username cannot be blank"), Length(max=30, message="Provide a first name of less than 30 characters")])
    last_name = StringField('Last name', validators=[InputRequired(message="Username cannot be blank"), Length(max=30, message="Provide a last name of less than 30 characters")])

class LoginUserForm(FlaskForm):
    """Form for users to login in the page"""

    username = StringField('Username', validators=[InputRequired(message="Username cannot be blank"), Length(max=20, message="Provide a username of less than 20 characters")])
    password = PasswordField('Password', validators=[InputRequired(message="Password cannot be blank")])

class AddFeedbackForm(FlaskForm):
    """Form to add some feedback for logged in users"""

    title = StringField('Title', [InputRequired(message="Title cannot be blank"), Length(max=100, message="Provide a title of less than 100 characters")])
    content = StringField('Content', [InputRequired(message="Content cannot be blank")])

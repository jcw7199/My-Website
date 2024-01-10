from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, EqualTo, Email

class SignUpForm(FlaskForm):
    firstName = StringField('First name', [DataRequired(message="Data required!")])
    lastName = StringField('Last name', [DataRequired(message="Data required!")])
    email = StringField('Email', [DataRequired(message="Data required!"), Email(), EqualTo('confirmEmail', message="Emails must match")])
    confirmEmail = StringField('Confirm Email', [DataRequired(message="Data required!"), EqualTo('email', message="Emails must match")])
    password = PasswordField('Password', [DataRequired(message="Data required!"), EqualTo('confirmPassword', message="Passwords must match")])
    confirmPassword = PasswordField('Confirm Password', [DataRequired(message="Data required!"), EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid Email")]) 
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit = SubmitField('Login') 

class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="Invalid Email")])
    submit = SubmitField('Reset Password') 

class PasswordResetForm(FlaskForm):
    newPassword = PasswordField('New Password', validators=[DataRequired(message="Data required!"), EqualTo('confirmNewPassword', message="Passwords must match")])
    confirmNewPassword = PasswordField('Confirm Passowrd', validators=[DataRequired(message="Data required!"), EqualTo('newPassword', message="Passwords must match")])
    submit = SubmitField('Save new Password')
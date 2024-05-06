from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import BooleanField
from wtforms.fields import PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, Optional

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


class AccountResetForm(FlaskForm):
    newFirstName = StringField('First name', validators=[EqualTo('confirmNewFirstName', message="First names must match")])
    newLastName = StringField('Last name', validators=[EqualTo('confirmNewLastName', message="Last names must match")])

    confirmNewFirstName = StringField('First name', validators=[EqualTo('newFirstName', message="First names must match")])
    confirmNewLastName = StringField('Last name', validators=[EqualTo('newLastName', message="Last names must match")])

    newEmail = StringField('New Email', validators=[Optional(), Email(message="Invalid Email"), EqualTo('confirmNewEmail', message="Emails must match")])
    confirmNewEmail = StringField('Confirm Email', validators=[Optional(), Email(message="Invalid Email"), EqualTo('newEmail', message="Emails must match")])

    newPassword = PasswordField('New Password', validators=[EqualTo('confirmNewPassword', message="Passwords must match")])
    confirmNewPassword = PasswordField('Confirm Passowrd', validators=[EqualTo('newPassword', message="Passwords must match")])

    submit = SubmitField('Save Changes')
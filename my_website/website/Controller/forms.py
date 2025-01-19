from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired, Email

class ContactMeForm(FlaskForm):
    firstName = StringField(label="First Name", validators=[DataRequired()])
    lastName = StringField(label="Last Name", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    subject = TextAreaField(label="Subject", validators=[DataRequired()])
    message = TextAreaField(label="Contact Me", validators=[DataRequired()])
    submit = SubmitField('Send')
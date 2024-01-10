from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class NewPasswordForm(FlaskForm):
    websiteAppName = StringField('Website or App name', validators=[DataRequired()]) 
    username = StringField('Username')
    email = StringField('Email', validators=[Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Save Password')
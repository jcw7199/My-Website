from dataclasses import dataclass
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from .. import mail
from flask_mail import Message

from .forms import ContactMeForm


routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template("home.html", user=current_user)

@routes.route('/resume')
def resume():
    return render_template("resume.html", user=current_user)


@routes.route('/cover_letter')
def coverLetter():
    return render_template("cover_letter.html", user=current_user)


@routes.route('/snake', methods=['GET'])
def snake():
    return render_template('snake.html', user=current_user)


@routes.route('/spotify', methods=['GET'])
def spotify():
    return render_template('spotify.html', user=current_user)

@routes.route('/contact_me', methods=['GET', 'POST'])
def contactMe():
    contactForm = ContactMeForm()

    if request.method == 'POST':
        if contactForm.validate_on_submit():
            msg = Message(contactForm.subject.data, recipients=['jordancw7199@gmail.com', contactForm.email.data], sender=contactForm.email.data)
            
            msg.body = contactForm.message.data + " " + " sent by " + contactForm.firstName.data + " " + contactForm.lastName.data + ". Email: " + contactForm.email.data
            mail.send(msg)
            flash("Message sent! A copy of your message has been emailed to you as well.", category='success')
    return render_template('contact_me.html', user=current_user, form=contactForm)
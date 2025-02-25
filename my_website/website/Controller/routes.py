from dataclasses import dataclass
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session, render_template_string
from flask_login import login_required, current_user
from .. import db
from .. import mail

from flask_mail import Message
from ..Model.models import SpotifyAuthCode
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


@routes.route('/storeAuthCode', methods=['GET'])
def storeSpotifyAuthCode():

    print("Your Computer IP Address is:" + request.remote_addr)
    print("BASE COOKIES: ", request.base_url)
    print("DATA COOKIES: ", request.data)
    print("PATH: " + request.full_path)

    ip = request.remote_addr
    auth_code = request.args.get('code')
    error = request.args.get('error')
    newCode = None

    if ip != None:

        oldCodes = SpotifyAuthCode.query.filter_by(ipAddr=ip).all()

        for code in oldCodes:
            print("DELETING OLD CODE")
            db.session.delete(code)






    if auth_code != None:
        newCode = SpotifyAuthCode(code=auth_code, ipAddr=ip)
    else:
        newCode = SpotifyAuthCode(code=error, ipAddr=ip)


    db.create_all()

    db.session.add(newCode)
    db.session.commit()

    #return {"code": newCode.code}
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Close Tab</title>
    </head>
    <body>
        <script>
            window.close();
        </script>
        <p>This tab will close automatically.</p>
    </body>
    </html>""")



@routes.route('/getAuthCode', methods=['GET'])
def getSpotifyAuthCode():


    print("Your Computer IP Address is:" + request.remote_addr)
    print("BASE COOKIES: ", request.base_url)
    print("DATA COOKIES: ", request.data)
    print("PATH: " + request.full_path)

    ip = request.remote_addr


    count = SpotifyAuthCode.query.filter_by(ipAddr=ip).count()

    auth_code = None
    if count > 0:

        auth_code = SpotifyAuthCode.query.filter_by(ipAddr=ip).first().code

        oldCodes = SpotifyAuthCode.query.filter_by(ipAddr=ip).all()

        for code in oldCodes:
            print("DELETING OLD CODE")
            db.session.delete(code)

        db.session.commit()
    else:
        auth_code = count

    return {'code': auth_code, 'IPAddr': ip}





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
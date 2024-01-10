from xml.dom.domreg import registered
from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..Model.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .auth_forms import LoginForm, SignUpForm, ForgotForm, PasswordResetForm
from .. import db
from .. import mail
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message

auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    
    sform = SignUpForm()
    #get data from sign up form
    if request.method == 'POST':
        if sform.validate_on_submit():            
            #query for user already existing in database before adding new user to database
            email = sform.email.data            
            registeredUser = User.query.filter_by(email=email).first()
            
            if registeredUser:
                flash('Email is already registered to an account', category='error')
            else:
            #create account
                newUser = User(
                            email = sform.email.data, 
                            firstName = sform.firstName.data, 
                            lastName = sform.lastName.data, 
                            password=generate_password_hash(sform.password.data, method='sha256')
                            ) 
                db.session.add(newUser)
                db.session.commit()
                login_user(newUser, remember=False)
                flash('Account created', category='success')
                return redirect(url_for('routes.home'))
    return render_template("sign_up.html", form = sform, user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    lform = LoginForm()
    if request.method == 'POST':
        if lform.validate_on_submit():
            email = lform.email.data
            
            password = lform.password.data
            user = User.query.filter_by(email=email).first()
            if user:
                print("user found")
                if check_password_hash(user.password, password):
                    login_user(user, remember=lform.remember_me)                    
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for("routes.home"))
                else:
                    flash('Incorrect email/password, please try again', category='error')
            else:
                print("user not found")
                flash('Incorrect email/password, please try again', category='error')
        else:
            print("form error")
    return render_template("login.html", form=lform, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

def send_mail(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='jordancw7199@gmail.com')
    msg.body = f''' To reset your password, please follow the link below.

        {url_for('auth.resetPassword', token=token, _external=True)}
        This link will expire in 10 minutes.
        
        If you didn't send a request to reset your password, please ignore this message.
    '''
    mail.send(msg)


@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgotPassword():
    forgotForm = ForgotForm()
    if forgotForm.validate_on_submit():
        user = User.query.filter_by(email=forgotForm.email.data).first()
        if user:
            send_mail(user)
            flash("Account found! Check email to reset password.")
            return redirect(url_for("routes.home"))
        else:
            flash("No account found with following email: " + forgotForm.email.data, category="error")
    return render_template("forgot_password.html", form=forgotForm, user=current_user)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def resetPassword(token):
    (email, error) = User.verify_token(token)
    
    if error:
        flash(error, category='error')
        return redirect(url_for("auth.login"))      
    else:
        user = User.query.filter_by(email = email).first()
        login_user(user)
        resetForm = PasswordResetForm()

        if resetForm.validate_on_submit():
            user.password = generate_password_hash(resetForm.newPassword.data, method='sha256')
            db.session.commit()
            flash("Password reset!", category="success")
            return redirect(url_for("auth.login"))
        
    return render_template("reset_password.html", form=resetForm, user=current_user)

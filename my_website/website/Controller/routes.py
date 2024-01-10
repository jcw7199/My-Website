from dataclasses import dataclass
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for 
from flask_login import login_required, current_user
from .. import db

from website.Model.models import SavedPassword
from .passwordManager_forms import NewPasswordForm

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template("home.html", user=current_user)

@routes.route('/resume')
def resume():
    return render_template("resume.html", user=current_user)    

@routes.route('/password_manager')
def passwordManager():
    return render_template("password_manager.html", user=current_user)

@routes.route('/save_password', methods=['GET', 'POST'])
@login_required
def savePassword():
    newPassForm = NewPasswordForm()

    if request.method == 'POST':
        if newPassForm.validate_on_submit():
            newPassword = SavedPassword(
                user_id = current_user.id,
                websiteAppName = newPassForm.websiteAppName.data,
                username = newPassForm.username.data,
                email = newPassForm.email.data,
                password = newPassForm.password.data                
            )

            db.session.add(newPassword)
            db.session.commit()
            flash("Password saved!", category='success')
            return redirect(url_for("routes.passwordManager"))
    return render_template("save_password.html", form=newPassForm, user=current_user)
    
@routes.route('/view_passwords', methods=['GET', 'POST'])
@login_required
def viewPasswords():
    return render_template('view_passwords.html', user=current_user)

@routes.route('/delete_SavedPassword/<password_id>', methods=['POST', 'DELETE'])
def deleteSavedPassword(password_id):
    password = SavedPassword.query.filter_by(id=password_id).first()
    db.session.delete(password)
    db.session.commit()
    flash("Password deleted!", category="success")
    return render_template('view_passwords.html', user=current_user)

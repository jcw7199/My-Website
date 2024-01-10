from .. import db
from .. import app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    savedPasswords = db.relationship('SavedPassword')

    def get_token(self):
        serial = Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_email':self.email})

    @staticmethod
    def verify_token(token):
        serial =  Serializer(app.config['SECRET_KEY'])
        error = None
        user_email = None
        try:
            user_email = serial.loads(token, max_age=600)['user_email']    
        except:
                error = "Reset password token expired."
        
        return (user_email, error)

class SavedPassword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    websiteAppName = db.Column(db.String(10000))
    username =  db.Column(db.String(10000)) 
    email = db.Column(db.String(10000))
    password = db.Column(db.String(10000))

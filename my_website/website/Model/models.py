from myapp import db, app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))

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


class SpotifyAuthCode(db.Model):
    code = db.Column(db.String(300), primary_key=True)
    ipAddr = db.Column(db.String(100), primary_key=True)
    def __str__(self):
         return "Code: " + self.code + "\n\nSession: " + self.ipAddr
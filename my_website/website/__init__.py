from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, urandom
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
DB_NAME = "database.db"

mail = Mail()

app = Flask(__name__, template_folder='View/templates')
app.config['SECRET_KEY'] = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'


db.init_app(app)

from .Controller.routes import routes
from .Controller.auth_routes import auth

from .Model.models import User

app.register_blueprint(routes, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))



def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("created database")

def create_mail():

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_DEFAULT_SENDER'] = 'jordancw7199@gmail.com'
    app.config['MAIL_USERNAME'] = 'jordancw7199@gmail.com'
    app.config['MAIL_PASSWORD'] = 'rzbwttwjetvwlazk'

    mail.init_app(app)

create_database(app)
create_mail()
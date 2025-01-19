from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, urandom
from flask_login import LoginManager
from flask_mail import Mail


DB_NAME = "database.db"


app = Flask(__name__, template_folder='View/templates',  static_folder='View/statics')
app.config['SECRET_KEY'] = urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy(app=app)

mail = Mail()
#db.init_app(app)

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



def create_database():
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
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

create_database()
create_mail()
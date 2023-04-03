from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = "database.db"

# Google Cloud SQL (change this accordingly)
PASSWORD ="(bmgA9{Ta>AahL~|"
PUBLIC_IP_ADDRESS ="34.96.225.89"
DBNAME ="database"
PROJECT_ID ="yttut"
INSTANCE_NAME ="big-keyword-382510:asia-east2:yttut"


def create_app():
    basedir = os.path.join(os.path.pardir, "tmp")
    print(basedir)
    #os.path.dirname(os.path.abspath(__file__))

    app = Flask(__name__)
    # future Greg - how to store this privately
    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    with app.app_context():
        db.create_all()

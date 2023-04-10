import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#import os

db = SQLAlchemy()

def create_app():
    # Google Cloud SQL (change this accordingly)
    PASSWORD = "gflask"
    PUBLIC_IP_ADDRESS = "35.220.170.13"
    DBNAME = "yttut"
    PROJECT_ID = "gflask-382913"
    INSTANCE_NAME = "gflask-382913:asia-east2:gflask"

    app = Flask(__name__)




    # configuration
    app.config["SECRET_KEY"] = "yoursecretkey"
    # removed   and {PROJECT_ID}: after password
    app.config[
        "SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://gflask:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{INSTANCE_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.init_app(app)

    from .models import User, Note



    with app.app_context():
        db.create_all()

    # basedir = os.path.join(os.path.pardir, "tmp")

    # # Initialise a client
    # storage_client = storage.Client("yttut")
    # # Create a bucket object for our bucket
    # bucket = storage_client.bucket("big-keyword-382510.appspot.com")
    # # Create a blob object from the filepath
    # blob = bucket.blob("database.db")
    # # Download the file to a destination
    # blob.download_to_filename("./tmp/database.db")
    # ######DB URI    mysql+mysqldb://root@/database?unix_socket=/cloudsql/yttut:yttut
    # #os.path.dirname(os.path.abspath(__file__))

    # # future Greg - how to store this privately
    # app.config['SECRET_KEY'] = 'mysecretkey'
    # #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + GCLOUD_DB
    # #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, DB_NAME)
    # #app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://root@/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///../tmp/{DB_NAME}'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

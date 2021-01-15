from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
import google.oauth2.credentials
import google_auth_oauthlib.flow


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
from . import routes
from . import api
app.register_blueprint(api.api_bp, url_prefix='/api')
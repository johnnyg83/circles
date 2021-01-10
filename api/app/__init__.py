from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
auth_client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])
print(app.config['GOOGLE_CLIENT_ID'])
from . import routes
from . import api
app.register_blueprint(api.api_bp, url_prefix='/api')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
from . import routes
from . import api
app.register_blueprint(api.api_bp, url_prefix='/api')
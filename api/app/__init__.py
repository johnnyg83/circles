from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
app = Flask(__name__)
db = SQLAlchemy(app)
from . import routes

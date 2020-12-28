from flask import Flask
app = Flask(__name__)


from api.app import routes

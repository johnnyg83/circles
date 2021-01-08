from flask.templating import render_template
from . import app, db
from.models import User

@app.route('/') 
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
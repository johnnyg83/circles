from . import app, db
from.models import User

@app.route('/')
def home():
    johnny_gundo = User(username='johnny_g', email='john.gunderson@yale.edu')
    db.create_all()
    db.session.add(johnny_gundo)
    db.session.commit()
    print(User.query.filter_by(username='johnny_g').first())

    return 'Hello World!'
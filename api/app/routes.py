from flask.templating import render_template
from . import app, db
from .models import User
from .models import InterestsTable

@app.route('/') 
def home():
    johnny_gundo = User(id='johnny_g', email='john.gunderson@yale.edu', online=True)
    chrissy_yaodo = User(id='chrissy_y', email='chris.yao@yale.edu', online=True)
    db.drop_all()
    db.create_all()
    db.session.commit()
    db.session.add(johnny_gundo)
    db.session.add(chrissy_yaodo)
    db.session.commit()

    johnny_gundo.addFriend(chrissy_yaodo)
    print(johnny_gundo.getFriends())
    chrissy_yaodo.deleteFriend(johnny_gundo)
    print(johnny_gundo.getFriends())
    print(johnny_gundo)
    johnny_gundo.logout()
    print(johnny_gundo)

    johnny_gundo.addInterest("tennis")
    chrissy_yaodo.addInterest("being epic")
    chrissy_yaodo.deleteInterest("sucking")
    print(chrissy_yaodo.getInterests())

    johnny_gundo.addInterest("tennis")
    johnny_gundo.addInterest("reading")
    print(johnny_gundo.getInterests())

    johnny_gundo.addInterest("meat tenderizing")
    print(johnny_gundo.getInterests())

    johnny_gundo.deleteInterest("meat tenderizing")
    print(johnny_gundo.getInterests())

    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

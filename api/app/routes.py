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

    johnny_gundo.add_friend(chrissy_yaodo)
    print(johnny_gundo.get_friends())
    chrissy_yaodo.delete_friend(johnny_gundo)
    print(johnny_gundo.get_friends())
    print(johnny_gundo)
    johnny_gundo.logout()
    print(johnny_gundo)

    johnny_gundo.add_interest("tennis")
    chrissy_yaodo.add_interest("being epic")
    chrissy_yaodo.delete_interest("sucking")
    print(chrissy_yaodo.get_interests())

    johnny_gundo.add_interest("tennis")
    johnny_gundo.add_interest("reading")
    print(johnny_gundo.get_interests())

    johnny_gundo.add_interest("meat tenderizing")
    print(johnny_gundo.get_interests())

    johnny_gundo.delete_interest("meat tenderizing")
    print(johnny_gundo.get_interests())

    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

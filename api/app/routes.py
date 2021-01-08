from . import app, db
from .models import User
from .models import InterestsTable

@app.route('/')
def home():
    johnny_gundo = User(username='johnny_g', email='john.gunderson@yale.edu')
    chrissy_yaodo = User(username='chrissy_y', email='chris.yao@yale.edu')
    db.create_all()
    db.session.add(johnny_gundo)
    db.session.add(chrissy_yaodo)
    db.session.commit()
    addUserInterest(johnny_gundo, "tennis")
    addUserInterest(chrissy_yaodo, "being epic")
    deleteUserInterest(chrissy_yaodo, "sucking")
    print(getUserInterests(chrissy_yaodo))

    addUserInterest(johnny_gundo, "tennis")
    addUserInterest(johnny_gundo, "reading")
    print(getUserInterests(johnny_gundo))
    addUserInterest(johnny_gundo, "meat tenderizing")
    print(getUserInterests(johnny_gundo))
    deleteUserInterest(johnny_gundo, "meat tenderizing")
    print(getUserInterests(johnny_gundo))

    return 'Hello World!'

def addUserInterest(user, interest):
    if len(InterestsTable.query.filter_by(id=user.id, interest=interest).all()) == 0:
        db.session.add(InterestsTable(id=user.id, interest=interest))
        db.session.commit()

def getUserInterests(user):
    return InterestsTable.query.filter_by(id=user.id).all()

def deleteUserInterest(user, interest):
    row = InterestsTable.query.filter_by(id=user.id, interest=interest).first()
    if row is not None:
        db.session.delete(row)
        db.session.commit()




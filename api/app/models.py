from . import db
class User(db.Document):
    username = db.StringField()
    email = db.StringField()
    image = db.StringField()
    interests = db.ListField()
    

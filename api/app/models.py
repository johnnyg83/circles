from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class InterestsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest = db.Column(db.String(1000), primary_key=True)

    def __repr__(self):
        return '<InterestsTable %r %r>' % (self.id, self.interest)

from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def addInterest(self, interest):
        if len(InterestsTable.query.filter_by(id=self.id, interest=interest).all()) == 0:
            db.session.add(InterestsTable(id=self.id, interest=interest))
            db.session.commit()

    def getInterests(self):
        return InterestsTable.query.filter_by(id=self.id).all()

    def deleteInterest(self, interest):
        row = InterestsTable.query.filter_by(id=self.id, interest=interest).first()
        if row is not None:
            db.session.delete(row)
            db.session.commit()
    
    def addFriend(self, friend):
        if len(FriendsTable.query.filter_by(id=self.id, friend_id=friend.id).all()) == 0:
            db.session.add(FriendsTable(id=self.id, friend_id=friend.id))
            db.session.commit()

    def getFriends(self):
        return FriendsTable.query.filter_by(id=self.id).all()

    def deleteFriend(self, friend):
        row = FriendsTable.query.filter_by(id=self.id, friend_id=friend.id).first()
        if row is not None:
            db.session.delete(row)
            db.session.commit()


class InterestsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    interest = db.Column(db.String(1000), primary_key=True)

    def __repr__(self):
        return '<InterestsTable %r %r>' % (self.id, self.interest)

class FriendsTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friend_id = db.Column(db.Integer, primary_key=True)

    # if username=='johnny_g':
    #     friends = 0

    def __repr__(self):
        return '<FriendsTable %r %r>' % (self.id, self.friend_id)


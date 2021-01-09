from . import db

class User(db.Model):
    id = db.Column(db.String(80), primary_key=True) #username
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=True)
    online = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<User %r %r %r>' % (self.id, self.email, self.online)

    def add_interest(self, interest):
        if len(InterestsTable.query.filter_by(id=self.id, interest=interest).all()) == 0:
            db.session.add(InterestsTable(id=self.id, interest=interest))
            db.session.commit()

    def get_interests(self):
        return [x.interest for x in InterestsTable.query.filter_by(id=self.id).all()]

    def delete_interest(self, interest):
        row = InterestsTable.query.filter_by(id=self.id, interest=interest).first()
        if row is not None:
            db.session.delete(row)
            db.session.commit()
    
    def add_friend(self, friend):
        if len(FriendsTable.query.filter_by(id=self.id, friend_id=friend.id).all()) == 0:
            db.session.add(FriendsTable(id=self.id, friend_id=friend.id))
            db.session.commit()

    def get_friends(self):
        return [x.friend_id for x in FriendsTable.query.filter_by(id=self.id).all()]

    def delete_friend(self, friend):
        row = FriendsTable.query.filter_by(id=self.id, friend_id=friend.id).first()
        if row is not None:
            db.session.delete(row)
            db.session.commit()
    
    def login(self):
        self.online = True
        db.session.commit()
    
    def logout(self):
        self.online = False
        db.session.commit()
    
    def get_all_data(self):
        data = {'id': self.id, 'email': self.email, 'image': self.image, 'online': self.online, 'interests': self.getInterests(), 
        'friends': self.getFriends()}
        return data


class InterestsTable(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    interest = db.Column(db.String(100), primary_key=True)

    def __repr__(self):
        return '<InterestsTable %r %r>' % (self.id, self.interest)

class FriendsTable(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    friend_id = db.Column(db.String(80), primary_key=True)

    # if username=='johnny_g':
    #     friends = 0

    def __repr__(self):
        return '<FriendsTable %r %r>' % (self.id, self.friend_id)


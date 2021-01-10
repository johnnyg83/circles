from . import db
from datetime import datetime as dt

class User(db.Model):
    id = db.Column(db.String(80), primary_key=True) #username
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_email(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
        
    def __repr__(self):
        return '<User %r %r %r %r %r>' % (self.id, self.email, self.name, self.authenticated, self.last_login)

    def get_id(self):
        return str(self.id)

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
    
    def block_user(self, user):
        if len(BlockedUsersTable.query.filter_by(id=self.id, blocked_user_id=user.id).all()) == 0:
            db.session.add(BlockedUsersTable(id=self.id, blocked_user_id=user.id))
            db.session.commit()

    def get_blocked_users(self): 
        """Return the other users who the user has blocked."""
        #if name=="chris": return Aruni.id
        return [x.blocked_user_id for x in BlockedUsersTable.query.filter_by(id=self.id).all()]
    
    def get_who_has_blocked(self): #sorry for awkward name
        """Return the other users who have blocked the user"""
        return [x.id for x in BlockedUsersTable.query.filter_by(blocked_user_id=self.id).all()]

    def unblock_user(self, user):
        row = BlockedUsersTable.query.filter_by(id=self.id, blocked_user_id=user.id).first()
        if row is not None:
            db.session.delete(row)
            db.session.commit()

    def add_match(self, match):
        db.session.add(MatchesTable(id=self.id, match_id=match.id, match_time=dt.now()))

    def get_matches(self):
        return [(x.match_id, x.match_time) for x in MatchesTable.query.filter_by(id=self.id).all()]
    
    def get_all_data(self):
        data = {'id': self.id, 'email': self.email, 'name': self.name, 'image': self.image, 
        'authenticated': self.authenticated, 'interests': self.get_interests(), 'friends': self.get_friends(), 
        "last_login": self.last_login, 'matches': self.get_matches(), 'blocked_users': self.get_blocked_users(),
        'who_has_blocked': self.get_who_has_blocked()}
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

class MatchesTable(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    match_id = db.Column(db.String(80), primary_key=True)
    match_time = db.Column(db.DateTime(), primary_key=True)

    def __repr__(self):
        return '<MatchesTable %r %r>' % (self.id, self.match_id, self.match_time)

class BlockedUsersTable(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    blocked_user_id = db.Column(db.String(80), primary_key=True)

    def __repr__(self):
        return '<BlockedUserTable %r %r>' % (self.id, self.blocked_user_id)
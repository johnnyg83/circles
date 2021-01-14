from . import db
from datetime import datetime as dt
from sqlalchemy.orm.exc import NoResultFound

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(80), primary_key=True) #username
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(120))
    last_login = db.Column(db.DateTime)
    authenticated = db.Column(db.Boolean, default=False, nullable=False)
    privacy_settings = db.Column(db.String(20), default="0", nullable=False) #could either be one number, or a "string array" of 1s and 0s for each setting

    interests = db.relationship("Interest", back_populates="user", cascade="all, delete")
    friends = db.relationship("Friend", back_populates="user", cascade="all, delete")
    matches = db.relationship("Match", back_populates="user", cascade="all, delete")
    blocked_users = db.relationship("BlockedUser", back_populates="user", cascade="all, delete")

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
    
    def is_banned(self):
        bans = get_banned_users()
        print(bans)
        for ban in bans:
            if self.id==ban[0] and dt.now() < ban[2]:
                return True
        return False
        
    def __repr__(self):
        return '<User %r %r %r %r %r>' % (self.id, self.email, self.name, self.authenticated, self.last_login)

    def get_id(self):
        return str(self.id)
    
    def update(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
            db.session.commit()
            return True
        return False

    def get_instance(self, model, **kwargs):
        """Return first instance found from model"""
        try:
            return db.session.query(model).filter_by(**kwargs).first()
        except NoResultFound:
            return

    def add_instance(self, model, **kwargs):
        instance = self.get_instance(model, **kwargs)
        if instance is None:
            instance = model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return True
        return False

    def delete_instance(self, model, **kwargs):
        instance = self.get_instance(model, **kwargs)
        if instance is not None:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False
    
    def get_all_instances(self, model, **kwargs):
        """Return a list of all instances in model that fit the kwargs"""
        return model.query.filter_by(**kwargs).all()

    def add_interest(self, interest, rank):
        max_interests = 25
        if len(self.interests) >= 25:
            return False
        return self.add_instance(Interest, user_id=self.id, interest=interest, rank=rank)

    def add_interests_from_list(self, list):
        for interest in list:
            self.add_interest(interest, 0)
            
    def get_interests(self):
        return [x.interest for x in self.interests]

    def delete_interest(self, interest, rank):
        return self.delete_instance(Interest, interest=interest, rank=rank)
    
    def add_friend(self, friend):
        instance = self.get_instance(Friend, user_id=self.id, friend_id=friend.id)
        if instance is None:
            instance = Friend(user_id=self.id, friend_id=friend.id, time=dt.now())
            db.session.add(instance)
            db.session.commit()
            return True
        return False

    def get_friends(self):
        return [(x.friend_id, x.time) for x in self.friends]

    def delete_friend(self, friend):
        return self.delete_instance(Friend, user_id=self.id, friend_id=friend.id)
    
    def block_user(self, blocked_user):
        return self.add_instance(BlockedUser, user_id=self.id, blocked_user_id=blocked_user.id)

    def get_blocked_users(self): 
        """Return the other users who the user has blocked."""
        #if name=="chris": return Aruni.id
        return [x.blocked_user_id for x in self.blocked_users]
    
    def get_blocked_by(self): #sorry for awkward name
        """Return the other users who have blocked the user"""
        return [x.user_id for x in self.get_all_instances(BlockedUser, blocked_user_id=self.id)]

    def unblock_user(self, blocked_user):
        return self.delete_instance(BlockedUser, user_id=self.id, blocked_user_id=blocked_user.id)

    def report_user(self, user, reason):
        return self.add_instance(Report, reporter_id=self.id, reported_id=user.id, time=dt.now(), reason=reason)

    def get_reported_users(self):
        """Return the other users who the user has reported."""
        return [(x.reported_id, x.time) for x in self.get_all_instances(Report, reporter_id=self.id)]

    def get_reported_by(self): #sorry for awkward name
        """Return the other users who have reported the user"""
        return [(x.reporter_id, x.time) for x in self.get_all_instances(Report, reported_id=self.id)]

    def add_match(self, match):
        return self.add_instance(Match, user_id=self.id, match_id=match.id, time=dt.now())

    def get_matches(self):
        return [(x.match_id, x.time) for x in self.get_all_instances(Match, user_id=self.id)]

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
        return True
    
    def get_all_data(self):
        data = {'id': self.id, 'email': self.email, 'name': self.name, 'image': self.image, 
        'authenticated': self.authenticated, 'interests': self.get_interests(), 'friends': self.get_friends(), 
        "last_login": self.last_login, 'matches': self.get_matches(), 
        'blocked_users': self.get_blocked_users(), 'blocked_by': self.get_blocked_by(), 
        'reported_users': self.get_reported_users(), 'reported_by': self.get_reported_by(),
        'banned': self.is_banned(), 'privacy_settings': self.privacy_settings}
        return data

class Interest(db.Model):
    __tablename__ = 'interests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'))
    interest = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="interests")

    def __repr__(self):
        return '<Interest %r %r %r>' % (self.user_id, self.interest, self.rank)

class Friend(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'))
    friend_id = db.Column(db.String(80), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="friends")

    # if username=='johnny_g':
    #     friends = 0

    def __repr__(self):
        return '<Friend %r %r %r>' % (self.user_id, self.friend_id, self.time)

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'))
    match_id = db.Column(db.String(80), nullable=False)
    time = db.Column(db.DateTime())

    user = db.relationship("User", back_populates="matches")


    def __repr__(self):
        return '<Match %r %r %r>' % (self.user_id, self.match_id, self.time)

class BlockedUser(db.Model):
    __tablename__ = 'blocked_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('users.id'))
    blocked_user_id = db.Column(db.String(80), nullable=False)

    user = db.relationship("User", back_populates="blocked_users")

    def __repr__(self):
        return '<BlockedUser %r %r>' % (self.user_id, self.blocked_user_id)

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.String(80))
    reported_id = db.Column(db.String(80))
    time = db.Column(db.DateTime())
    reason = db.Column(db.String(120))

    def __repr__(self):
        return '<Report %r %r %r %r>' % (self.reported_id, self.reporter_id, self.time, self.reason)

class BannedUser(db.Model):
    __tablename__ = 'banned_users'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    time_banned = db.Column(db.DateTime())
    time_unbanned = db.Column(db.DateTime(), nullable=False)
    reason = db.Column(db.String(120))

    def __repr__(self):
        return '<BannedUser %r %r %r %r>' % (self.user_id, self.time_banned, self.time_unbanned, self.reason)

def ban_user(user_id, time_unbanned, reason):
    if BannedUser.query.filter_by(user_id=user_id, time_banned=dt.now(), time_unbanned=time_unbanned, reason=reason).first() is None:
        db.session.add(BannedUser(user_id=user_id, time_banned=dt.now(), time_unbanned=time_unbanned, reason=reason))
        db.session.commit()
        return True
    return False

def unban_user(user_id):
    bans = BannedUser.query.filter(BannedUser.user_id==user_id, BannedUser.time_unbanned > dt.now())
    #TODO may need to fix this? getattr and setattr are things idk ill figure it out later
    for ban in bans:
        ban.time_unbanned = dt.now()
        print('unban: ', ban)
    db.session.commit()
    return True

def get_banned_users():
    return [(x.user_id, x.time_banned, x.time_unbanned) for x in BannedUser.query.all()]
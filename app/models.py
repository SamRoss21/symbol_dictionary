from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    concepts = db.relationship('Concept', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Concept(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concept = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship(User)
    # search_words = db.relationship('SearchWord', backref='category', lazy='dynamic')
    num_im = db.Column(db.Integer)
    verified = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Concept {}>'.format(self.concept)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
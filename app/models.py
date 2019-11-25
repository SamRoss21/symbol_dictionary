from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
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
    concept = db.Column(db.String(140), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship(User)
    search_words = db.relationship('SearchWord', backref='category', lazy='dynamic')
    images = db.relationship('Image', backref='symbols', lazy='dynamic')
    num_im = db.Column(db.Integer)
    verified = db.Column(db.String(1))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.String(1))

    def __repr__(self):
        return '<Concept {}>'.format(self.concept)

class SearchWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    searchWord = db.Column(db.String(140), unique=True)
    brainstorm = db.Column(db.String(1))
    concept = db.Column(db.String(140))
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'))
    concepts = db.relationship(Concept)
    images = db.relationship('Image', backref='term', lazy='dynamic')
    num_im = db.Column(db.Integer)
    verified = db.Column(db.String(1))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.String(1))

    def __repr__(self):
        return '<SearchWord {}>'.format(self.searchWord)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(2000), unique=True)
    searchWord = db.Column(db.String(140))
    searchWord_id = db.Column(db.Integer, db.ForeignKey('search_word.id'))
    searchWords = db.relationship(SearchWord)
    concept = db.Column(db.String(140))
    concept_id = db.Column(db.Integer, db.ForeignKey('concept.id'))
    concepts = db.relationship(Concept)
    verified = db.Column(db.String(1))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    deleted = db.Column(db.String(1))

    def __repr__(self):
        return '<Image {}>'.format(self.image)
        
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
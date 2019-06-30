from app import db
from flask_login import UserMixin

from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
        return self.password_hash == password

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Book(db.Model):
    isbn = db.Column(db.Numeric(20), primary_key=True)
    title = db.Column(db.String(256), index=True)
    author = db.Column(db.String(256), index=True)
    year = db.Column(db.Integer, index=True)
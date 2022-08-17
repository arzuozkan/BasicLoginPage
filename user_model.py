from __init__ import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# db user model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), index=False, unique=True, nullable=False)
    email = db.Column(db.String(20), index=True, unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = set_password(password)


# password storage
def set_password(password):
    return generate_password_hash(password, method='sha256')


# password validation
def check_password(self, password):
    return check_password_hash(self.password, password)


def __repr__(self):
    return '<User {}>'.format(self.username)

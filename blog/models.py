from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize the db
db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define the relationship to User (one-to-many)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Define the relationship to Post (one-to-many)
    posts = db.relationship('Post', back_populates='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

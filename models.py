from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# User's table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(255))
    password = db.Column(db.String(100))

# Book's table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    total_pages = db.Column(db.Integer)

    user_books = db.relationship('UserBook', backref='book', cascade='all, delete-orphan')

# Relational table between Users and Books
class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add a cascade effect on deletion
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    current_page = db.Column(db.Integer)
    description = db.Column(db.String(255)) 

    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
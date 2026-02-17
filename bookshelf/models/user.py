from flask_login import UserMixin
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from bookshelf.db import db

class User(UserMixin, db.Model):
    id:  Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(100))

    def create_user(username, name, password):
        user = User(username=username, name=name, password=password) 
        db.session.add(user)
        db.session.commit()
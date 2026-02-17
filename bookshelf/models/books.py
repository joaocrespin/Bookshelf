from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from bookshelf.db import db
from datetime import datetime


class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    total_pages: Mapped[int] = mapped_column(Integer)
    user_books: Mapped[list["UserBook"]] = relationship( back_populates="book", cascade="all, delete-orphan")

# Relational table between Users and Books
class UserBook(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"))

    current_page: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(300))
    start_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_update: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    book: Mapped["Book"] = relationship(back_populates="user_books")
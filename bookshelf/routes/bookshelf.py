from flask import request, render_template, flash, redirect, url_for, Blueprint
from bookshelf.models.books import UserBook, Book
from flask_login import current_user, login_required
from bookshelf.db import db

bookshelf = Blueprint('bookshelf', __name__, '')

@bookshelf.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        
        title = request.form.get("title")
        current = int(request.form.get("current"))
        total = int(request.form.get("total"))
        description = request.form.get("description")

        if not title:
            flash("Title can't be empty", "danger")
            return redirect(url_for("bookshelf.add"))
        
        if not current or not total:
            flash("Pages can't be empty", "danger")
            return redirect(url_for("bookshelf.add"))

        if current > total:
            flash("Current page must be less or equal than the total number of pages", "danger")
            return redirect(url_for("bookshelf.add"))

        print(f"Title: {title} \nCurrent: {current} \nTotal: {total} \nDescription: {description}")

        # Creating the book
        new_book = Book(title=title, total_pages=total)
        db.session.add(new_book)
        db.session.commit()

        # Associating the book to the logged user
        user_book = UserBook(user_id=current_user.id, book_id=new_book.id, current_page=current, description=description)
        db.session.add(user_book)
        db.session.commit()

        return redirect(url_for("bookshelf.index"))
    
    return render_template("add.html")

@bookshelf.route("/delete/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):

    # Find the selected book by it's id
    book = Book.query.filter_by(id=book_id).first()

    # If the book doesn't exist, return an error
    if not book:
        flash("Book not found.", "warning")
        return redirect(url_for("bookshelf.index"))

    # If the book's owner is not the user, return an error
    user_book = UserBook.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if not user_book:
        flash("You do not have permission to delete this book.", "danger")
        return redirect(url_for("bookshelf.index"))

    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()

    flash("Book deleted sucessfully!", "success")
    return redirect(url_for("bookshelf.index"))

@bookshelf.route("/edit/<int:book_id>", methods=["GET","POST"])
@login_required
def edit_book(book_id):

    # Find the selected book by it's id
    user_book  = UserBook.query.filter_by(book_id=book_id).first()

    if request.method == "POST":
        title = request.form.get("title")
        current = int(request.form.get("current"))
        total = int(request.form.get("total"))
        description = request.form.get("description")

        if not title:
            flash("You still need a title", "danger")
            return redirect(url_for("bookshelf.add"))
        
        if not current or not total:
            flash("Don't forget about the pages", "danger")
            return redirect(url_for("bookshelf.add"))

        if current > total:
            flash("Current page must be less or equal than the total number of pages.", "danger")
            return redirect(url_for("bookshelf.add"))
        
        # Changes the selected book values to new ones
        user_book.book.title = title
        user_book.current_page = current
        user_book.book.total_pages = total
        user_book.description = description

        db.session.commit()
        
        return redirect(url_for("bookshelf.index"))

    # Stores book data in a disctionary
    book = {
        'id': user_book.book_id,
        'title': user_book.book.title,
        'total_pages': user_book.book.total_pages,
        'current_page': user_book.current_page,
        'description': user_book.description
    }

    return render_template("edit.html", book=book)

# Temporarily here
@bookshelf.route("/")
@login_required
def index():

    # Queries the UserBook table to find the user's registered books
    user_books  = UserBook.query.filter_by(user_id=current_user.id).all()
    
    books=[]
    for user_book in user_books:
        
        # Add a dictionary into the list
        books.append({
            'id': user_book.book_id,
            'title': user_book.book.title,
            'total_pages': user_book.book.total_pages,
            'current_page': user_book.current_page,
            'description': user_book.description,
            'start_date': user_book.start_date
        })

    return render_template("index.html", name=current_user.name, books=books)


@bookshelf.route("/about")
def about():
    return render_template("about.html")
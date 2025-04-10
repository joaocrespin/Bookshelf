from flask import Flask, request, render_template, flash, redirect, url_for
from models import db, User, Book, UserBook
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
 
# Initialize Flask and SQL Alchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"

# Temporary key area
app.secret_key = "Jotasky"

# Flask_login setup
login_manager = LoginManager()

# Remove the message if the user is not authenticated
login_manager.login_message = None

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

# Load user based on session id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ADD A PAGE TO MANAGE THE USER


@app.route("/")
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if a field is empty
        if not username or not password:
            flash("Username or password must not be empty", "danger")
            return redirect(url_for("login"))

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        # If user was not found
        if not user or not check_password_hash(user.password, password):
            flash("Username or password incorrect", "danger")
            return redirect(url_for("login"))
        
        # If it passed the checks, login the user
        login_user(user)
        
        return redirect(url_for("index"))
    
    return render_template("login.html")

# Signup route  
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            flash("Username can't be empty", "danger")
            return redirect(url_for("signup"))
        
        if not name:
            flash("Name can't be empty", "danger")
            return redirect(url_for("signup"))
        
        if not password or not confirmation:
            flash("Passwords can't be empty", "danger")
            return redirect(url_for("signup"))
        
        if password != confirmation:
            flash("Passwords don't match", "danger")
            return redirect(url_for("signup"))
        
        # Verify if the username is already in use
        username_check = User.query.filter_by(username=username).first()

        # If username already in use redirect to the signup page
        if username_check:
            flash("Username already in use", "danger")
            return redirect(url_for(signup))
        
        hashed_password = generate_password_hash(password)

        # Create a new account
        user = User(username=username, name=name, password=hashed_password) 

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        
        title = request.form.get("title")
        current = int(request.form.get("current"))
        total = int(request.form.get("total"))
        description = request.form.get("description")

        if not title:
            flash("Title can't be empty", "danger")
            return redirect(url_for("add"))
        
        if not current or not total:
            flash("Pages can't be empty", "danger")
            return redirect(url_for("add"))

        if current > total:
            flash("Current page must be less or equal than the total number of pages", "danger")
            return redirect(url_for("add"))

        print(f"Title: {title} \nCurrent: {current} \nTotal: {total} \nDescription: {description}")

        # Creating the book
        new_book = Book(title=title, total_pages=total)
        db.session.add(new_book)
        db.session.commit()

        # Associating the book to the logged user
        user_book = UserBook(user_id=current_user.id, book_id=new_book.id, current_page=current, description=description)
        db.session.add(user_book)
        db.session.commit()

        return redirect(url_for("index"))
    
    return render_template("add.html")

@app.route("/delete/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):

    # Find the selected book by it's id
    book = Book.query.filter_by(id=book_id).first()

    # If the book doesn't exist, return an error
    if not book:
        flash("Book not found.", "warning")
        return redirect(url_for("index"))

    # If the book's owner is not the user, return an error
    user_book = UserBook.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    if not user_book:
        flash("You do not have permission to delete this book.", "danger")
        return redirect(url_for("index"))

    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()

    flash("Book deleted sucessfully!", "success")
    return redirect(url_for("index"))

@app.route("/edit/<int:book_id>", methods=["GET","POST"])
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
            return redirect(url_for("add"))
        
        if not current or not total:
            flash("Don't forget about the pages", "danger")
            return redirect(url_for("add"))

        if current > total:
            flash("Current page must be less or equal than the total number of pages.", "danger")
            return redirect(url_for("add"))
        
        # Changes the selected book values to new ones
        user_book.book.title = title
        user_book.current_page = current
        user_book.book.total_pages = total
        user_book.description = description

        db.session.commit()
        
        return redirect(url_for("index"))

    # Stores book data in a disctionary
    book = {
        'id': user_book.book_id,
        'title': user_book.book.title,
        'total_pages': user_book.book.total_pages,
        'current_page': user_book.current_page,
        'description': user_book.description
    }

    return render_template("edit.html", book=book)

@app.route("/about")
def about():
    return render_template("about.html")
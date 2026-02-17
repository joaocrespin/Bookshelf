from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from bookshelf.models.user import User

auth = Blueprint("auth", __name__, "/auth")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if a field is empty
        if not username or not password:
            flash("Username or password must not be empty", "danger")
            return redirect(url_for("auth.login"))

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        # If user was not found
        if not user or not check_password_hash(user.password, password):
            flash("Username or password incorrect", "danger")
            return redirect(url_for("auth.login"))
        
        # If it passed the checks, login the user
        login_user(user)
        
        return redirect(url_for("bookshelf.index"))
    
    return render_template("login.html")

# Signup route  
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":

        username = request.form.get("username")
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            flash("Username can't be empty", "danger")
            return redirect(url_for("auth.signup"))
        
        if not name:
            flash("Name can't be empty", "danger")
            return redirect(url_for("auth.signup"))
        
        if not password or not confirmation:
            flash("Passwords can't be empty", "danger")
            return redirect(url_for("auth.signup"))
        
        if password != confirmation:
            flash("Passwords don't match", "danger")
            return redirect(url_for("auth.signup"))
        
        # Verify if the username is already in use
        username_check = User.query.filter_by(username=username).first()

        # If username already in use redirect to the signup page
        if username_check:
            flash("Username already in use", "danger")
            return redirect(url_for(signup))
        
        hashed_password = generate_password_hash(password)

        # Create a new account
        User.create_user(username, name, hashed_password)
        
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("bookshelf.index"))

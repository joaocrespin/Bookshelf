from flask import Flask
from bookshelf.db import db, login_manager 
from bookshelf.config import config
from .models.user import User 
# Apparently it needs these imported to create the complete database
from .models.books import UserBook, Book

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.secret_key = config.SECRET_KEY

    db.init_app(app)
    with app.app_context():
        db.create_all() 

    login_manager.init_app(app)

    login_manager.login_view = "auth.login" 
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.bookshelf import bookshelf
    from .routes.auth import auth
    app.register_blueprint(bookshelf)
    app.register_blueprint(auth)

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

# Extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

from blog.models import db, Post, User

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    migrate.init_app(app, db)

    # Register blueprints (if any)
    from blog.app import main  # Import your route blueprints here
    app.register_blueprint(main)

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
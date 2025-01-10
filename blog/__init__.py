from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

from blog.models import db, Post

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (if any)
    from blog.app import main  # Import your route blueprints here
    app.register_blueprint(main)

    return app

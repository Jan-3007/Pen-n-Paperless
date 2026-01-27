import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy




db = SQLAlchemy()




def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='frontend')
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    # Register routes and ensure DB exists
    with app.app_context():
        # import modules that register routes and characters
        from .game.character.character import Character  # noqa: F401
        from . import routes  # noqa: F401
        from . import db_setup
        db_setup.init_db()

    return app

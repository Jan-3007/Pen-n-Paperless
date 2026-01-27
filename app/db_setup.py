from . import db
from flask import current_app


def init_db():
    # Create database file's parent directory if needed
    import os
    db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    db.create_all()

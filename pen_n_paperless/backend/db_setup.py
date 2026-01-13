# Python module imports
import os

# Project internal imports
from .. import db, database_path


def init_db():
    # Create database file's parent directory if needed
    if not os.path.exists(database_path):
        os.makedirs(database_path, exist_ok=True)

    # Create database
    db.create_all()



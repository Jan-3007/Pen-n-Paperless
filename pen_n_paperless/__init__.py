# main package

# Python module imports
import os
from pathlib import Path
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# internal module imports
from .config.general import GeneralConfig
from .common.pyjs_shared_enums import CommonEnumGenerator


# Define database
db = SQLAlchemy()

# Define globally available paths
module_root_path = os.path.dirname(__file__)
database_path = os.path.join(module_root_path, "data", "db")
avatars_path = Path(module_root_path) / "frontend" / "static" / "avatars"


def create_app():

    # create paths
    avatars_path.mkdir(parents=True, exist_ok=True)

    # Define log file path
    log_file = os.path.join(module_root_path, "logs", "pen-n-paperless.log")

    # Define logging behaviour
    logging.basicConfig(
        filename = log_file,
        encoding = 'utf-8',
        filemode = 'a',
        level = GeneralConfig.log_level(),
        format = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
    )

    # Define all paths needed for app setup
    template_path = os.path.join(module_root_path, "frontend", "templates")
    static_path = os.path.join(module_root_path, "frontend", "static")

    # Create the app
    app = Flask(
        __name__, 
        template_folder=template_path, 
        static_folder=static_path

    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(database_path, 'pen-n-paperless.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    app.config['avatars'] = avatars_path.as_posix()


    db.init_app(app)

    # Register routes and ensure DB exists
    with app.app_context():
        # import modules that register routes and characters
        from .backend import routes
        from .backend.characters.characters import Character  # noqa: F401
        from .backend.db_setup import init_db
        init_db()

    return app




def generate_files():
    # export all keys
    python_enum_file = Path(__file__).parent / 'common' / 'keys.py'
    js_enum_file = Path(__file__).parent / 'frontend' / 'static' / 'js' / 'enums.js'

    with CommonEnumGenerator(   python_file_path=python_enum_file.absolute().as_posix(), 
                                js_file_path=js_enum_file.absolute().as_posix()
                            ) as common_enum_generator:

        common_enum_generator.generate()

    # export status codes
    python_enum_file = Path(__file__).parent / 'common' / 'status_codes.py'
    js_enum_file = Path(__file__).parent / 'frontend' / 'static' / 'js' / 'status_codes.js'

    with CommonEnumGenerator(   python_file_path=python_enum_file.absolute().as_posix(), 
                                js_file_path=js_enum_file.absolute().as_posix()
                            ) as common_enum_generator:

        common_enum_generator.generate()

    print("Generating files completed.")
    return
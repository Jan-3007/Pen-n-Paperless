# connection point between web pages (frontend) and the python scripts (backend)

# Python module imports
import os
from flask import current_app as app
from flask import   session,\
                    render_template,\
                    url_for,\
                    request,\
                    redirect,\
                    flash
import glob


# internal imports
from .routes_helpers import *

from .. import module_root_path, avatars_path
from ..config.general import GeneralConfig
from ..common.keys import Generic

from pen_n_paperless.backend.characters import *

from pen_n_paperless.content import *


# done for now
@app.route('/')
def main():
    """(route) Main page: Gets called when a user access the root url

    If the user is still logged in as a character, the character will be shown on the main page.

    The main page displays all existing characters.
    Page includes a form to create a new character.
    """

    session_char_id = get_active_character_id()
    active_character = None
    avatar_url = None

    # show the active character on the main page, skip if none can be found
    if session_char_id:
        active_character = get_character_by_id(character_id=session_char_id)
        if active_character:
            logging.info(f'"{active_character.name}" already logged in.')
        
            # try to find avatar file
            avatar_url = get_avatar_path(session_char_id, active_character.name)
        else:
            logging.error(f"Found ID '{session_char_id}' in session, but no associated character found in database.")
            flash("Internal error", "error")

    # get all available characters for the main page
    characters = get_all_characters()

    # get avatar path for each character
    character_dict = {}
    for ch in characters:
        character_dict[ch.name] = get_avatar_path(ch.id, ch.name)

    # render main page
    return render_template(
        # template
        'main.html',
        # generic
        language = GeneralConfig.language(),
        world_name = GeneralConfig.world_name(),
        # active character
        active_character = active_character,
        avatar_url = avatar_url,
        # all characters
        character_dict = character_dict
    )


# done for now
@app.route('/login', methods=['POST'])
def login_or_create():
    """(route) in-between page: for logging in and creating new characters

    Login is possible by creating a form with an invisible input field with the parameters:
        - name = "name"
        - value = "<character_name>"
    This form also includes a submit button for the user to initiate the login.

    Character creation is enabled by creating a form with a text input (text is default type) with the parameters:
        - name = "name"
        - no default value
    In order for the user to initiate the creation and login process, the form includes a submit button as well.
    """

    if request.method == 'POST':
        
        # get string from text input or value from hidden input
        name = request.form.get("name", "").strip()

        if name == "":
            logging.error(f'Error, character name cannot be empty.')
            flash('Please provide a character name', 'error')
            return redirect(url_for('main'))
        
        existing = get_character_by_name(name)
        if existing:
            # create new session with the existing character
            session[Generic.ID.value] = existing.id
            logging.info(f'Logging user in as "{existing.name}" with ID: {existing.id}.')
            return redirect(url_for('character_overview', character_name=existing.name))

        # create a new character
        new_character = create_character(name)
        if new_character:
            session[Generic.ID.value] = new_character.id
            logging.info(f'Created new character "{new_character.name}" with ID: {new_character.id}.')
            logging.info(f'Logging user in as "{new_character.name}" with ID: {new_character.id}.')
            return redirect(url_for('character_overview', character_name=new_character.name))

        else:
            logging.error(f'login_or_create(): Requested character name was "{name}", not "", could not resolve name to an existing character, failed to create a new character using the name')
            
    else:
        logging.error(f'login_or_create(): Unexpected request method, got: {request.method}')

    logging.critical(f'login_or_create(): Unexpected behaviour, returning to the main page.')
    flash(f'Internal error', 'error')
    return redirect(url_for('main'))





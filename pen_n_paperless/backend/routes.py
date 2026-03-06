# connection point between web pages (frontend) and the python scripts (backend)

# Python module imports
import os
from flask import current_app as app
from flask import   session,\
                    request,\
                    render_template,\
                    url_for,\
                    redirect,\
                    flash,\
                    send_from_directory,\
                    get_flashed_messages

import logging

# internal imports
from .routes_helpers import get_active_character_id


from pen_n_paperless.config.general import GeneralConfig
from pen_n_paperless.config.character import CharacterConfig

import pen_n_paperless.common.keys as keys

from pen_n_paperless.backend.characters import  *

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
    if session_char_id >= 0:
        active_character = get_character_by_id(character_id=session_char_id)
        if active_character:
            logging.info(f'"{active_character.name}" already logged in.')
        
            # try to find avatar file
            avatar_url = active_character.avatar.file_url if active_character.avatar else ""
        else:
            logging.error(f"Found ID '{session_char_id}' in session, but no associated character found in database.")
            flash("Internal error", "error")

    # get all available characters for the main page
    characters = get_all_characters()

    # get avatar path for each character
    character_dict = {}
    for ch in characters:
        character_dict[ch.name] = ch.avatar.file_url if ch.avatar else ""

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
            session[keys.Generic.ID.value] = existing.id
            logging.info(f'Logging user in as "{existing.name}" with ID: {existing.id}.')
            flash(f'Logged in as {existing.name}', 'success')
            return redirect(url_for('character_overview', character_name=existing.name))

        # create a new character
        new_character = create_character(name)
        if new_character:
            session[keys.Generic.ID.value] = new_character.id
            logging.info(f'Created new character "{new_character.name}" with ID: {new_character.id}.')
            logging.info(f'Logging user in as "{new_character.name}" with ID: {new_character.id}.')
            flash(f'Logged in as {new_character.name}', 'success')

            return redirect(url_for('character_overview', character_name=new_character.name))

        else:
            logging.error(f'login_or_create(): Requested character name was "{name}", not "", could not resolve name to an existing character, failed to create a new character using the name')
            
    else:
        logging.error(f'login_or_create(): Unexpected request method, got: {request.method}')

    logging.critical(f'login_or_create(): Unexpected behaviour, returning to the main page.')
    flash(f'Internal error', 'error')
    return redirect(url_for('main'))


# done for now
# call this page with 'url_for('logout')'
@app.route('/logout', methods=['POST'])
def logout():
    """(route) in-between page: for logging out

    Logout will happen by simply removing the character ID from the users session if it is available.
    After removing it, the user will be redirected back to the main page.
    """

    if request.method == 'POST':

        id = session.pop(keys.Generic.ID.value, None)

        char_id = session.get(keys.Generic.ID.value, None)
        if char_id is not None:
            logging.error(f'logout(): Error while logging out. Failed to remove character ID from session. \n\tCharacter ID: {char_id}.')
            flash(f'Internal error.', 'error')
            return redirect(url_for('main'))
        
        logging.info(f'User with character ID "{id}" has logged out.')
        flash('Logged out', 'success')

    else:
        logging.error(f'logout(): Unexpected request method, got: {request.method}')
        flash(f'Internal error', 'error')

    return redirect(url_for('main'))




# character pages

# <character_name> is dynamically replaced with the actual character name
# call this page with 'url_for('character_overview', character_name=name)'
@app.route('/<string:character_name>')
def character_overview(character_name: str):
    """(route) Character overview page: Page after successfully logging in

    When a user tries to access this page without being logged in they will be send back to main.
    If the user tries to access a character page while being logged in as another character, they will be send back to their own page.
    
    :param character_name: Name of the character
    :type character_name: str
    """

    logging.debug(f'character_overview(): page for {character_name} requested')
    
    session_char_id = get_active_character_id()
    logging.debug(f'character_overview(): got character ID {session_char_id} from session')

    # User is not logged in as a character
    if session_char_id == None:
        logging.error(f'Error while trying to access page: /{character_name}. User not signed in.')
        flash("Please sign in first", "error")
        return redirect(url_for('main'))
    
    # Resolve character from ID
    character_from_session = get_character_by_id(session_char_id)
    if character_from_session == None:
        logging.error(f'character_overview(): Error while resolving character ID.')
        flash(f'Internal error.', 'error')
        return redirect(url_for('main'))
    
    # User is logged in, but <character_name> does not match the name retrieved using the ID from the session
    if character_name != character_from_session.name:
        logging.error(f'User tried to access page of a different character whilst being logged in. \n\tCharacter from session: {character_from_session.id}, {character_from_session.name}. \n\tRequested character: "{character_name}"')
        flash(f'Please log out first.', 'error')
        return redirect(url_for('character_overview', character_name=character_from_session.name))
    
    # try to find avatar
    avatar_url = character_from_session.avatar.file_url if character_from_session.avatar else ""

    logging.info(f"Character {character_from_session.name} is accessing its overview.")

    return render_template(
        # template
        'character.html',
        # generic
        language = GeneralConfig.language(),
        keys = keys,
        # character
        character = character_from_session,
        avatar_url = avatar_url,
        tribe_dict = Tribe.get_all_names(),
        profession_dict = Profession.get_all_names(),
        specialization_dict = Specialization.get_available(character_from_session.profession, character_from_session.level),
        # Armour, Weapons
        max_armour_sets = CharacterConfig.max_armour_sets(),
        armour_dict = Armoury.get_all_names(),
        max_nb_weapons = CharacterConfig.max_number_of_weapons(),
        weapons_dict = Weaponry.get_all_names()
        # Abilities
        # ability_dict = 
    )



# character subpages

# call this page with 'url_for('editor', character_name=name)'
@app.route('/<string:character_name>/editor')
def editor(character_name: str):
    """(route) Character editor page

    When a user tries to access this page without being logged in they will be send back to main.
    If the user tries to access a character page while being logged in as another character, they will be send back to their own page.
    
    :param character_name: Name of the character
    :type character_name: str
    """

    logging.debug(f'character_overview(): retrieving character ID from session')
    session_char_id = get_active_character_id()

    # User is not logged in as a character
    if session_char_id == None:
        logging.error(f'Error while trying to access page: /{character_name}/editor. User not signed in accordingly.')
        flash("Please sign in first", "error")
        return redirect(url_for('main'))

    # Resolve character from ID
    character_from_session = get_character_by_id(session_char_id)
    if character_from_session == None:
        logging.error(f'editor(): Error while resolving character ID.')
        flash(f'Internal error.', 'error')
        return redirect(url_for('main'))
    
    # User is logged in, but <character_name> does not match the name retrieved using the ID from the session, not allowed
    if character_name != character_from_session.name:
        logging.error(f'User tried to access a character page whilst being logged in as another character. \n\tCharacter ID from session: {character_from_session.id}. \n\tRequested character: "{character_name}"')
        flash(f'Please log out first.', 'error')
        return redirect(url_for('character_overview', character_name=character_from_session.name))
    
    # try to find avatar file
    avatar_url = character_from_session.avatar.file_url if character_from_session.avatar else ""

    logging.info(f"Character {character_from_session.name} is accessing its editor.")

    # TODO: provide lists of max_armour_sets, max_nb_weapons, ...
    return render_template(
        # template
        'character_editor.html',
        # generic
        language = GeneralConfig.language(),
        keys = keys,
        # character
        character = character_from_session,
        avatar_url = avatar_url,
        avatar_dimensions = GeneralConfig.avatar_size(),
        tribe_dict = Tribe.get_all_names(),
        profession_dict = Profession.get_all_names(),
        specialization_dict = Specialization.get_available(character_from_session.profession, character_from_session.level),
        # Armour, Weapons
        max_armour_sets = CharacterConfig.max_armour_sets(),
        armour_dict = Armoury.get_all_names(),
        max_nb_weapons = CharacterConfig.max_number_of_weapons(),
        weapons_dict = Weaponry.get_all_names()
    )




# call this page with 'url_for('edit', character_name=name)'
@app.route('/<string:character_name>/edit', methods=['POST'])
def edit(character_name: str) -> dict:
    """(route) Character edit request page

    When the user changes a value, the data is sent here to be processed.

    When a user tries to access this page without being logged in they will be send back to main.
    
    :param character_name: Name of the character
    :type character_name: str
    """

    if request.method != 'POST':
        logging.error(f'Unexpected request method, got: {request.method}')
        flash(f'Internal error', 'error')
        return {'status' : 'error', 'flashed' : get_flashed_messages(with_categories=True)}
        # return redirect(url_for('main'))


    logging.debug(f'retrieving character ID from session')
    session_char_id = get_active_character_id()

    # User is not logged in as a character
    if session_char_id == None:
        logging.error(f'Error while trying to access page: /{character_name}/editor. User not signed in accordingly.')
        flash("Please sign in first", "error")
        return {'status' : 'error', 'flashed' : get_flashed_messages(with_categories=True)}
        # return redirect(url_for('main'))

    # Resolve character from ID
    character_from_session = get_character_by_id(session_char_id)
    if character_from_session == None:
        logging.error(f'Error while resolving character ID.')
        flash(f'Internal error.', 'error')
        return {'status' : 'error', 'flashed' : get_flashed_messages(with_categories=True)}
        # return redirect(url_for('main'))

    
    # User is logged in, but <character_name> does not match the name retrieved using the ID from the session, not allowed
    if character_name != character_from_session.name:
        logging.error(f'User tried to access a character page whilst being logged in as another character. \n\tCharacter ID from session: {character_from_session.id}. \n\tRequested character: "{character_name}"')
        flash(f'Please log out first.', 'error')
        return {'status' : 'error', 'flashed' : get_flashed_messages(with_categories=True)}
        # return redirect(url_for('character_overview', character_name=character_from_session.name))


    # get the json data from the html request as a dict
    new_data = request.get_json() or {}
    if new_data == {}:
        logging.error(f'failed to retrieve data from request.')
        flash(f'Internal error', 'error')
        return {'status' : 'error', 'flashed' : get_flashed_messages(with_categories=True)}

    # send new data to character
    update = character_from_session.edit(new_data)

    update['flashed'] = get_flashed_messages(with_categories=True)
    return update














# call this page with 'url_for('delete', character_name=name)'
@app.route('/<string:character_name>/delete')
def delete(character_name = None):

    logging.debug(f'edit(): retrieving character ID from session')
    session_char_id = get_active_character_id()

    # User is not logged in as a character
    if session_char_id == None:
        logging.error(f'Error while trying to access page: /{character_name}/editor. User not signed in accordingly.')
        flash("Please sign in first", "error")
        return redirect(url_for('main'))

    # Resolve character from ID
    character_from_session = get_character_by_id(session_char_id)
    if character_from_session == None:
        logging.error(f'edit(): Error while resolving character ID.')
        flash(f'Internal error.', 'error')
        return redirect(url_for('main'))
    
    # User is logged in, but <character_name> does not match the name retrieved using the ID from the session, not allowed
    if character_name != character_from_session.name:
        logging.error(f'User tried to access a character page whilst being logged in as another character. \n\tCharacter ID from session: {character_from_session.id}. \n\tRequested character: "{character_name}"')
        flash(f'Please log out first.', 'error')
        return redirect(url_for('main'))


    # remove ID from session
    session.pop(keys.Generic.ID.value, None)

    # TODO: overkill?
    char_id = session.get(keys.Generic.ID.value, None)
    if char_id is not None:
        logging.error(f'delete(): Error while deleting a character. Failed to remove character with ID {session_char_id} from session.')
        flash(f'Internal error.', 'error')
        return redirect(url_for('main'))

    # delete character from db
    success = delete_character(session_char_id)
    if not success:
        logging.error(f'delete(): Error while deleting a character. Failed to remove character with ID {session_char_id} from database.')
        flash(f'Internal error', 'error')
        return redirect(url_for('main'))
    
    logging.info(f'delete(): Successfully deleted character with ID: {session_char_id}.')
    flash(f'Character deleted successfully', 'success')
    return redirect(url_for('main'))




# favico.ico for older browsers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

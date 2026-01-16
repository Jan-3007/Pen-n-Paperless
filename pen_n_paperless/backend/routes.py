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


# internal imports
from .routes_helpers import *

from .. import module_root_path, avatars_path
from ..config.general import GeneralConfig
from ..common.keys import Generic

from .characters.characters import *




# done for now
@app.route('/')
def main():
    """(route) Main page: Gets called when a user access the root url

    If the user is still logged in as a character, the character will be shown on the main page.

    The main page displays all existing characters.
    Page includes a form to create a new character.
    """

    character_id = get_active_character_id()
    active_character = None
    avatar_url = None

    # show the active character on the main page, skip if none can be found
    if character_id:
        active_character = get_character_by_id(character_id=character_id)
        if active_character:
            logging.info(f'"{active_character.name}" already logged in.')
        
            # try to find avatar file
            avatar_url = get_avatar_path(character_id, active_character.name)
        else:
            logging.error(f"Found ID '{character_id}' in session, but no associated character found in database.")
            flash("Internal error", "error")

    # get all available characters for the main page
    characters = get_all_characters()

    # render main page
    return render_template(
        # template
        'main.html',
        # generic
        world_name = GeneralConfig.world_name,
        # active character
        active_character = active_character,
        avatar_url = avatar_url,
        # all characters
        characters = characters
    )


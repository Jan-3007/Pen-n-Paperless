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
from .. import avatars_path
from ..common.keys import Generic

from .characters.characters import *






def get_active_character_id() -> int | None:
    """
    Docstring for get_active_character_id
    
    :return: The ID of the currently active character, or None if no character is active
    :rtype: int | None
    """
    return session.get(Generic.ID.value, None)

def get_avatar_path(character_id: int, character_name: str) -> str:

    # prefer webp if present
    webp_path = os.path.join(avatars_path, f'{character_id}_{character_name}.webp')
    if os.path.exists(webp_path):
        return url_for('static', filename=f'images/avatars/{character_id}_{character_name}.webp')
    else:
        # search for any type of file with the expected name
        pattern = os.path.join(avatars_path, f'{character_id}_{character_name}.*')
        matches = glob.glob(pattern)
        if matches:
            filename = os.path.basename(matches[0])
            return url_for('static', filename=f'images/avatars/{filename}')
    
    logging.warning(f'get_avatar_path(): searching avatar for id "{character_id}" with name "{character_name}", did not find a match.')
    return ""

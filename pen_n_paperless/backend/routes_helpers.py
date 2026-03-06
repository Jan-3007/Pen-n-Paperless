# Python module imports
import os
from flask import   session

from typing import Callable


# internal imports
from ..common.keys import Generic




# avatar filename definition
avatar_filename: Callable[[int, str], str] = lambda character_id, character_name: (f'{character_id}_{character_name}')


def get_active_character_id() -> int:
    """
    Docstring for get_active_character_id
    
    :return: The ID of the currently active character, or None if no character is active
    :rtype: int | None
    """

    return session.get(Generic.ID.value, -1)






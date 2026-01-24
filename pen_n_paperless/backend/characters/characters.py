# character main class


# Python module imports
import logging
from sqlalchemy.orm import  Mapped 
from typing import List

# internal imports
from ... import db







class Character(db.Model):
    __tablename__ = "table_characters"


    # _id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    _name = db.Column(db.String(100), default="")


    def __init__(self, display_name: str):
        self._name = display_name
        return

    def __str__(self) -> str:
        return f"Hi. My name is {self._name}."
    

    # Properties
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    # @name.setter
    # def name(self, new_display_name: str):
    #     self._name = new_display_name
    #     db.session.commit()
    #     return
    



# global helper functions
def get_character_by_name(name: str) -> Character | None:
    """
    Docstring for get_character_by_name
    
    :param name: Name of the character to search for.
    :type name: str
    :return: Returns the first found character that matches the given name.
    :rtype: Character
    """
    # TODO: prevent duplicates from case-sensitivity
    return Character.query.filter_by(_name=name).first()


def get_character_by_id(character_id: int) -> Character | None:
    """
    Docstring for get_character_by_id
    
    :param character_id: ID of the character to search for.
    :type character_id: int
    :return: Returns the character that is associated with the given ID.
    :rtype: Character | None
    """
    # TODO: decide get() or get_or_404()
    return Character.query.get(character_id)


def get_all_characters() -> List[Character]:
    """List of all existing characters
    
    :return: List of all available characters.
    :rtype: List[Character]
    """
    return Character.query.order_by(Character._name).all()


def character_exists(character_id: int) -> bool:
    """
    Docstring for character_exists
    
    :param character_id: The character ID to check for if it exists already
    :type character_id: int
    :return: Returns True if the character with the specified ID already exists
    :rtype: bool
    """

    if Character.query.get(character_id):
        return True

    return False


def create_character(name: str) -> Character | None:
    """
    Internal error logging.
    
    :param name: The display name of the new character.
    :type name: str
    :return: The created character.
    :rtype: Character
    """

    logging.debug(f'Request to create new character with the name: "{name}".')

    c = Character(
            display_name = name
        )
    db.session.add(c)
    db.session.commit()
    
    if character_exists(c.id):
        logging.info(f'New character created. \n \t {c.name}: "{c}"')
        return c
    else:
        logging.error(f'Error while trying to create a new character "{name}"".')
        return None


def delete_character(character_id: int) -> bool:
    """
    Internal error logging.
    
    :param character_id: The ID of the character to be deleted permanently.
    :type character_id: int
    :return: Returns True if deletion was successful
    :rtype: bool
    """

    c = Character.query.get(character_id)
    temp_name = ""
    temp_id = -1
    logging.debug(f'Request to delete character with ID: {character_id}')
    
    if c is not None:
        temp_name = c.name
        temp_id = c.id

        db.session.delete(c)
        db.session.commit()

    success = character_exists(character_id=character_id)
    if not success:
        logging.info(f'Character "{temp_name}" with ID {temp_id} deleted.')
    else:
        logging.error(f'Error while trying to delete character with ID: {character_id}.')

    return success




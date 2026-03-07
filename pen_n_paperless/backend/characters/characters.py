# character main class


# Python module imports
import logging
from typing import List

from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import  Enum,\
                        String,\
                        Integer,\
                        Text,\
                        PickleType,\
                        ForeignKey
                        
from sqlalchemy.orm import  relationship,\
                            Mapped,\
                            mapped_column

from flask import flash

# internal imports
from pen_n_paperless import db

from pen_n_paperless.common.status_codes import StatusCode
from pen_n_paperless.common.keys import get_enum_values,\
                                        Generic,\
                                        Tribes, \
                                        Professions, \
                                        Specializations,\
                                        Armour,\
                                        Weapons

from pen_n_paperless.config.character import CharacterConfig    
from pen_n_paperless.config.general import GeneralConfig      

from .attributes import Attributes
from .history import History

from .avatars import Avatar

from pen_n_paperless.content.characters.tribe import Tribe
from pen_n_paperless.content.characters.profession import Profession
from pen_n_paperless.content.characters.specialization import Specialization

class Character(db.Model):
    __tablename__ = "table_characters"


    _id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    _name: Mapped[str] = mapped_column(String(100), default="")

    # Avatar
    _avatar = None

    # Tribe, Profession and Specialization
    _tribe: Mapped[Tribes] = mapped_column(Enum(Tribes, values_callable=get_enum_values), nullable=True, default=None)
    _profession: Mapped[Professions] = mapped_column(Enum(Professions, values_callable=get_enum_values), nullable=True, default=None)
    _specialization: Mapped[Specializations] = mapped_column(Enum(Specializations, values_callable=get_enum_values), nullable=True, default=None)

    # Statistics
    _level: Mapped[int] = mapped_column(Integer, default=1)
    _max_hp: Mapped[int] = mapped_column(Integer, default=100)

    # Attributes - one-to-one relationship
    _attributes: Mapped["Attributes"] = relationship("Attributes", back_populates='_character', uselist=False)

    # Abilities
    # TODO: Abilities instance

    # Armour
    # _defense_bonus: Mapped[int] = mapped_column(Integer, default=0)
    _equipped_armour: Mapped[List] = mapped_column(MutableList.as_mutable(PickleType), default=list)

    # Weapons
    _equipped_weapons: Mapped[List] = mapped_column(MutableList.as_mutable(PickleType), default=list)

    # Notes
    _notes: Mapped[str] = mapped_column(Text, default='')

    # HP and XP history
    # HP history is element 0, XP history is element 1
    # associate the history table in a many-to-one relationship
    _histories: Mapped[List[History]] = relationship("History", back_populates='_character')


# -------------------------------------------------------------------------------

    def __init__(self, display_name: str) -> None:
        self._name = display_name
        self._attributes = Attributes()
        self._histories.append(History("HP"))
        self._histories.append(History("XP"))

        self._equipped_armour = [Armour.ARMOUR] * CharacterConfig.max_armour_sets()
        self._equipped_weapons = [Weapons.WEAPON] * CharacterConfig.max_number_of_weapons()

        return

    def __str__(self) -> str:
        return f"Hi. My name is {self.name}."


# -------------------------------------------------------------------------------

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

    # Avatar
    @property
    def avatar(self) -> Avatar | None:
        if self._avatar is None:
            self._avatar = Avatar(self.id, self.name)

        return self._avatar
    
    # Tribe, Profession and Specialization
    @property
    def tribe(self) -> Tribes:
        # conversion from str back to Tribes is handled by SQLAlchemy
        return self._tribe
    @property
    def profession(self) -> Professions:
        return self._profession
    @property
    def specialization(self) -> Specializations:
        return self._specialization

    # Statistics
    @property
    def level(self) -> int:
        return self._level
    @property
    def experience(self) -> int:
        return self.xp_history.get_total()
    @property
    def max_hp(self) -> int:
        return self._max_hp
    @property
    def current_hp(self) -> int:
        return self.max_hp - self.hp_history.get_total()

    # Attributes
    @property
    def attributes(self) -> dict:
        return self._attributes.get_attributes()
    @property
    def attribute_bonuses(self) -> dict:
        return self._attributes.get_attribute_bonuses()
    @property
    def attribute_points(self) -> dict:
        return {
            Generic.TOTAL_POINTS: self._attributes.total_points,
            Generic.USED_POINTS: self._attributes.used_points,
            Generic.REMAINING_POINTS: self._attributes.remaining_points
        }
    # when setting attributes, call _update_max_hp, _update_attribute_bonuses

    # Armour
    # @property
    # def defense_bonus(self) -> int:
    #     return self._defense_bonus
    @property
    def equipped_armour(self) -> list:
        return self._equipped_armour
    
    # # Weapons
    @property
    def equipped_weapons(self) -> list:
        return self._equipped_weapons
    
    # Notes
    @property
    def notes(self) -> str:
        return self._notes

    # Histories
    @property
    def hp_history(self) -> History:
        return self._histories[0]
    @property
    def xp_history(self) -> History:
        return self._histories[1]

    # Abilities


# -------------------------------------------------------------------------------

    # public methods
    def edit(self, received_data: dict) -> dict:
        """Change data of a Character instance

        The data can contain one or more key-value-pairs. A key specifies the attribute whose value is to be changed.
        For example:
        {
            Generic.NOTES : "Hello World"
        }

        :param new_data: The key with the data to be changed.
        :type new_data: dict
        :return: Returns a dict with data for immediate UI updates or if the webpage should be fully reloaded.
        :rtype: dict
        """

        # collect updated values to return to the client for immediate UI update
        data_to_send = {}
        # set default values
        data_to_send.setdefault('reload', False)
        data_to_send.setdefault(StatusCode.STATUS.value, StatusCode.ERROR.value)
        
        status = StatusCode.ERROR

        for key in received_data.keys():
            # the key will be the value of the enum entry, see common/keys and common/pyjs_shared_enums

            if key == Generic.NOTES.value:
                new_notes = received_data.get(key, '')
                self._notes = new_notes
                status = StatusCode.SUCCESS
                logging.debug(f'Changed data in notes to "{new_notes[0:10]}..."')
                # no need to send data back, input field stores the latest data

            elif key == Tribes.TRIBE.value:
                data = received_data.get(key, {})
                data_key = data.get('key', '')
                data_value = data.get('value', '')

                try:
                    data_key = Tribes(data_key)
                except ValueError as e:
                    logging.error(f'key {key} is invalid, exc: {e}')
                    flash(f'Internal error', 'error')
                    break
                status = self._edit_tribe(data_key, data_value)

                data_to_send[key] = {
                    "key": self.tribe.value,
                    "value": Tribe.get_name(self.tribe)
                }

            elif key == Professions.PROFESSION.value:
                data = received_data.get(key, {})
                data_key = data.get('key', '')
                data_value = data.get('value', '')

                try:
                    data_key = Professions(data_key)
                except ValueError as e:
                    logging.error(f'key {key} is invalid, exc: {e}')
                    flash(f'Internal error', 'error')
                    break
                status = self._edit_profession(data_key, data_value)

                data_to_send[key] = {
                    "key": self.profession.value,
                    "value": Profession.get_name(self.profession)
                }

                # trigger a page reload
                data_to_send.update({'reload' : True})

            elif key == Specializations.SPECIALIZATION.value:
                data = received_data.get(key, {})
                data_key = data.get('key', '')
                data_value = data.get('value', '')

                try:
                    data_key = Specializations(data_key)
                except ValueError as e:
                    logging.error(f'key {key} is invalid, exc: {e}')
                    flash(f'Internal error', 'error')
                    break
                status = self._edit_specialization(data_key, data_value)

                data_to_send[key] = {
                    "key": self.specialization.value,
                    "value": Specialization.get_name(self.specialization, self.level)
                }

            else:
                # stop proccessing as soon as a key cannot be found
                status = StatusCode.ERROR.value

                logging.error(f'key {key} is invalid')
                flash(f'Internal error', StatusCode.ERROR.value)
                break


        if status != StatusCode.ERROR:
            # all data has been processed successfully, commit and overwrite defaults
            db.session.commit()
            data_to_send.update({StatusCode.STATUS.value : str(status)})

        return data_to_send
        


    # private methods
    def _edit_tribe(self, tribe_key: Tribes, tribe_name: str = '') -> StatusCode:

        if tribe_key not in Tribe.get_all():
            logging.error(f'Tribe key {tribe_key} is invalid')
            flash(f'Internal error', StatusCode.ERROR.value)
            return StatusCode.ERROR

        self._tribe = tribe_key
        logging.debug(f'Changed tribe to "{tribe_name if tribe_name else Tribe.get_properties(tribe_key).get(Generic.NAME, 'error')}"')

        # _update_attribute_bonuses()
        # _update_defense_bonus()
        return StatusCode.SUCCESS
    
    def _edit_profession(self, profession_key: Professions, profession_name: str = '') -> StatusCode:

        if profession_key not in Profession.get_all():
            logging.error(f'Profession key {profession_key} is invalid')
            flash(f'Internal error', StatusCode.ERROR.value)
            return StatusCode.ERROR

        self._profession = profession_key
        # delete specialization if the profession has been changed
        # counts as deleted as long as it is not a distinct specialization
        self._specialization = Specializations.SPECIALIZATION
        logging.debug(f'Changed profession to "{profession_name if profession_name else Tribe.get_properties(profession_key).get(Generic.NAME, {}).get(GeneralConfig.language(), 'error')}"')

        # _update_max_hp()
        # _update_attribute_bonuses()
        # _update_defense_bonuses()
        return StatusCode.SUCCESS

    def _edit_specialization(self, specialization_key: Specializations, specialization_name: str = '') -> StatusCode:

        if specialization_key not in Specialization.get_available(self.profession, self.level).keys():
            logging.error(f'Specialization key {specialization_key} is invalid')
            flash(f'Internal error', StatusCode.ERROR.value)
            return StatusCode.ERROR
        
        if specialization_name != '' and specialization_name not in Specialization.get_all_names().keys():
            # valid key, but name is not valid, send warning but let it pass
            logging.warning(f'User [{self.id}, {self.name}] tried to set the locked specialization "{specialization_key}"')
            flash(f'Not available', StatusCode.WARNING.value)
            return StatusCode.WARNING

        self._specialization = specialization_key
        logging.debug(f'Changed specialization to "{specialization_name if specialization_name else Specialization.get_properties(specialization_key).get(Generic.NAME, {}).get(GeneralConfig.language(), 'error')}"')

        # _update_attribute_bonuses()
        # _update_defense_bonus()
        return StatusCode.SUCCESS
# -------------------------------------------------------------------------------

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


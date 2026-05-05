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
                                        Weapons,\
                                        Attributes as AttributeKeys,\
                                        Statistics,\
                                        History as HistoryKeys

from pen_n_paperless.config.character import CharacterConfig    
from pen_n_paperless.config.general import GeneralConfig      

from .attributes import Attributes
from .history import History

from .avatars import Avatar

from pen_n_paperless.content.characters.tribe import Tribe
from pen_n_paperless.content.characters.profession import Profession
from pen_n_paperless.content.characters.specialization import Specialization

# from pen_n_paperless.content.items.armoury import Armoury

from pen_n_paperless.content import *

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
    _total_attribute_bonuses: dict = {}

    # Abilities
    # TODO: Abilities instance

    # Armour
    # _defense_bonus: Mapped[int] = mapped_column(Integer, default=0)
    _equipped_armour: Mapped[List] = mapped_column(MutableList.as_mutable(PickleType), default=list)
    _total_defense_bonus: dict = {}

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

        self._update_attribute_bonuses()
        # self._update_max_hp()

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
        return self._total_attribute_bonuses
    @property
    def attribute_points(self) -> dict:
        return {
            Generic.TOTAL_POINTS: self._attributes.total_points,
            Generic.USED_POINTS: self._attributes.used_points,
            Generic.REMAINING_POINTS: self._attributes.remaining_points
        }
    # when setting attributes, call _update_max_hp, _update_attribute_bonuses

    # Armour
    @property
    def defense_bonus(self) -> dict:
        return self._total_defense_bonus
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

        The data can contain one or more categories. 
        Each category contains data for changing the character property.
        For example:
        {
            HistoryKeys.XP_HISTORY: {
                Generic.DESCRIPTION: "some string",
                Generic.VALUE: 0
            }
        }
        will add a new history entry to the characters xp history.

        :param received_data: Contains the data to be applied.
        :type received_data: dict
        :return: Returns a dict with data for immediate UI updates or if the webpage should be fully reloaded.
        :rtype: dict
        """

        # collect updated values to return to the client for immediate UI update
        data_to_send = {}
        # set default values
        data_to_send.setdefault('reload', False)
        data_to_send.setdefault(StatusCode.STATUS.value, StatusCode.ERROR.value)
        
        status = StatusCode.ERROR

        for category_key in received_data.keys():
            # the key will be the value of the enum entry, see common/keys and common/pyjs_shared_enums

            match category_key:
                case Generic.NOTES.value:
                    # TODO revise internal data from received_data to adopt new data layout definition
                    new_notes = received_data.get(category_key, '')
                    self._notes = new_notes
                    status = StatusCode.SUCCESS
                    logging.debug(f'Changed data in notes to "{new_notes[0:10]}..."')
                    # no need to send data back, input field stores the latest data

                case Tribes.TRIBE.value:
                    data: dict = received_data.get(category_key, {})

                    data_key, data_value = data.popitem()
                    # convert key to Enum type
                    try:
                        data_key = Tribes(data_key)
                    except ValueError as e:
                        logging.error(f'key {data_key} is invalid, exc: {e}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break
                    status = self._edit_tribe(data_key, data_value)

                    data_to_send[category_key] = {
                        self.tribe.value: Tribe.get_name(self.tribe)
                    }

                case Professions.PROFESSION.value:
                    data = received_data.get(category_key, {})

                    data_key, data_value = data.popitem()
                    # convert key to Enum type
                    try:
                        data_key = Professions(data_key)
                    except ValueError as e:
                        logging.error(f'key {data_key} is invalid, exc: {e}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break
                    status = self._edit_profession(data_key, data_value)

                    data_to_send[category_key] = {
                        self.profession.value: Profession.get_name(self.profession)
                    }

                    # trigger a page reload
                    data_to_send.update({'reload' : True})

                case Specializations.SPECIALIZATION.value:
                    data = received_data.get(category_key, {})

                    data_key, data_value = data.popitem()
                    # convert key to Enum type
                    try:
                        data_key = Specializations(data_key)
                    except ValueError as e:
                        logging.error(f'key {data_key} is invalid, exc: {e}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break
                    status = self._edit_specialization(data_key, data_value)

                    data_to_send[category_key] = {
                        self.specialization.value: Specialization.get_name(self.specialization, self.level)
                    }

                case AttributeKeys.ATTRIBUTE.value:
                    data = received_data.get(category_key, {})
                    data_key, data_value = data.popitem()

                    # convert key to Enum type
                    try:
                        data_key = AttributeKeys(data_key)
                    except ValueError as e:
                        logging.error(f'key {data_key} is invalid, exc: {e}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break
                    status = self._attributes.modify_attribute(data_key, data_value)

                    self._update_attribute_bonuses()

                    # data_key can only be an attribute, other_data_key is then a bonus
                    bonus_data_key = self._attributes.convert_key(data_key)

                    # TODO: change to send all values for the bonus
                    data_to_send[category_key] = {
                        data_key.value: self.attributes.get(data_key, -1),
                        bonus_data_key.value: self.attribute_bonuses.get(bonus_data_key, {}).get(data_key, {}).get(Generic.VALUE.value, -1),
                        Generic.REMAINING_POINTS.value: self._attributes.remaining_points
                    }

                case HistoryKeys.HP_HISTORY.value:
                    data = received_data.get(category_key, {})
                    print(f"HP: {data}")

                    if Generic.VALUE.value in data.keys() and Generic.DESCRIPTION.value in data.keys():
                        # add entry to history
                        succ = self.hp_history.add_entry(data.get(Generic.VALUE.value, 0), data.get(Generic.DESCRIPTION.value, ''))
                        if not succ:
                            break

                    elif HistoryKeys.ENTRY_NUMBER.value in data.keys():
                        # remove entry from history
                        succ = self.hp_history.delete_entry(data.get(HistoryKeys.ENTRY_NUMBER.value, -1))
                        if not succ:
                            logging.error(f'Failed to delete entry nb. {data.get(HistoryKeys.ENTRY_NUMBER.value, -1)} in HP history of "{self.name}"')
                            break
                    
                    else:
                        logging.error(f'Keys in data did not match for creation or deletion of an HP history entry. Got keys {data.keys()}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break
                    
                    status = StatusCode.SUCCESS
                    # trigger a page reload
                    data_to_send.update({'reload' : True})

                case HistoryKeys.XP_HISTORY.value:
                    data = received_data.get(category_key, {})
                    print(f"XP: {data}")

                    if Generic.VALUE.value in data.keys() and Generic.DESCRIPTION.value in data.keys():
                        # add entry to history
                        print(f"add {data.get(Generic.VALUE.value, 0)}, {data.get(Generic.DESCRIPTION.value, '')}")
                        succ = self.xp_history.add_entry(data.get(Generic.VALUE.value, 0), data.get(Generic.DESCRIPTION.value, ''))
                        if not succ:
                            break

                    elif HistoryKeys.ENTRY_NUMBER.value in data.keys():
                        # remove entry from history
                        print(f"remove {data.get(HistoryKeys.ENTRY_NUMBER.value, -1)}")
                        succ = self.xp_history.delete_entry(data.get(HistoryKeys.ENTRY_NUMBER.value, -1))
                        if not succ:
                            logging.error(f'Failed to delete entry nb. {data.get(HistoryKeys.ENTRY_NUMBER.value, -1)} in XP history of "{self.name}"')
                            break

                    else:
                        logging.error(f'Keys in data did not match for creation or deletion of an XP history entry. Got keys {data.keys()}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break

                    status = StatusCode.SUCCESS
                    # trigger a page reload
                    data_to_send.update({'reload' : True})

                case Armour.ARMOUR.value:
                    data = received_data.get(category_key, {})

                    idx = data.pop(Generic.ID.value, -1)
                    if not idx in range(0, len(self._equipped_armour)):
                        logging.error(f'Armour index {idx} is out of range')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break

                    armour_key, armour_name = data.items()
                    # no need to check the name itself, only available armour will ever be displayed
                    try:
                        armour_key = Armour(armour_key)
                    except ValueError as e:
                        logging.error(f'key {armour_key} is invalid, exc: {e}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break

                    self._equipped_armour[idx] = armour_key

                    status = StatusCode.SUCCESS
                    data_to_send[category_key] = {
                        self.equipped_armour[idx].value: Armoury.get_name(self.equipped_armour[idx]),
                        Generic.ID.value: idx
                    }

                case Weapons.WEAPON.value:
                    data = received_data.get(category_key, {})

                    idx = data.pop(Generic.ID.value, -1)
                    if not idx in range(0, len(self._equipped_weapons)):
                        logging.error(f'Weapon index {idx} is out of range')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break

                    weapon_key, weapon_name = data.items()
                    # no need to check the name itself, only available armour will ever be displayed
                    try:
                        weapon_key = Weapons(weapon_key)
                    except ValueError as e:
                        logging.error(f'key {weapon_key} is invalid, exc: {e}')
                        flash(f'Internal error', StatusCode.ERROR.value)
                        break

                    self._equipped_weapons[idx] = weapon_key

                    status = StatusCode.SUCCESS
                    data_to_send[category_key] = {
                        self.equipped_weapons[idx].value: Weaponry.get_name(self.equipped_weapons[idx]),
                        Generic.ID.value: idx
                    }



                # TODO Abilities

                case _:
                    # stop proccessing as soon as a key cannot be found
                    status = StatusCode.ERROR

                    logging.error(f'key {category_key} is invalid')
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
        logging.debug(f'[Change] New tribe is "{tribe_name if tribe_name else Tribe.get_properties(tribe_key).get(Generic.NAME, 'error')}"')

        self._update_attribute_bonuses()
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
        logging.debug(f'[Changed] New profession is "{profession_name if profession_name else Tribe.get_properties(profession_key).get(Generic.NAME, {}).get(GeneralConfig.language(), 'error')}"')

        self._update_attribute_bonuses()
        self._update_max_hp()
        return StatusCode.SUCCESS

    def _edit_specialization(self, specialization_key: Specializations, specialization_name: str = '') -> StatusCode:

        if specialization_key not in Specialization.get_available(self.profession, self.level).keys():
            logging.error(f'Specialization key {specialization_key} is invalid')
            flash(f'Internal error', StatusCode.ERROR.value)
            return StatusCode.ERROR
        
        if specialization_name != '' and specialization_name not in Specialization.get_all_names().keys():
            # valid key, but name is not valid, send warning but let it pass
            logging.warning(f'User [{self.id}, {self.name}] tried to set the locked specialization "{specialization_key}"')
            flash(f'Locked', StatusCode.WARNING.value)
            return StatusCode.WARNING

        self._specialization = specialization_key
        logging.debug(f'[Change] New specialization is "{specialization_name if specialization_name else Specialization.get_properties(specialization_key).get(Generic.NAME, {}).get(GeneralConfig.language(), 'error')}"')

        self._update_attribute_bonuses()
        return StatusCode.SUCCESS
    

    # TODO work in the names as dict keys again
    def _update_attribute_bonuses(self) -> StatusCode:
        """Calculate the attribute bonus from all properties of the character.
        
        This class collects all bonuses from all viable sources and adds them up.

        An example for the returned dict:
        all = {
            bonus1: {
                attribute: 1,
                tribe: 0,
                profession: -1,
                armour: 2,
                total: 2
            },
            bonus2: {
                attribute: 2,
                tribe: -1,
                profession: 0,
                armour: 0,
                total: 1
            }
        }

        The keys will be stored as display names. Their only purpose is to be displayed in the info.
        """
        for bonus_key, bonus_val in self._attributes.get_attribute_bonuses().items():
            total_bonus = 0
            tmp = {}

            # bonus from attribute
            # the attribute class only stores the bonus calculated directly from the attribute, calculation was executed when the attribute was set
            attribute_key = self._attributes.convert_key(bonus_key)
            total_bonus += bonus_val
            tmp[attribute_key] = {
                Generic.NAME.value: Attributes.get_name(attribute_key),
                Generic.VALUE.value: bonus_val
            }
            # TODO: adapt following just as attribute
            # bonus from tribe
            next_bonus = Tribe.get_properties(self.tribe).get(bonus_key, 0)
            total_bonus += next_bonus
            tmp[Tribe.get_name(self.tribe)] = next_bonus

            # bonus from profession
            next_bonus = Profession.get_properties(self.profession).get(bonus_key, 0)
            total_bonus += next_bonus
            tmp[Profession.get_name(self.profession)] = next_bonus

            # bonus from specialization
            next_bonus = Specialization.get_attribute_bonus(self.specialization, self.level, bonus_key, 0)
            total_bonus += next_bonus
            tmp[Specialization.get_name(self.specialization, self.level)] = next_bonus

            # bonus from weapons
            for weapon in self.equipped_weapons:
                next_bonus = Weaponry.get_properties(weapon).get(bonus_key, 0)
                total_bonus += next_bonus
                tmp[Weaponry.get_name(weapon)] = next_bonus

            # bonus from armour
            for armour in self.equipped_armour:
                armour_bonus = Armoury.get_properties(armour).get(bonus_key, 0)
                total_bonus += armour_bonus
                tmp[Armoury.get_name(armour)] = armour_bonus

            # store result of current attribute bonus calculation
            tmp[Generic.TOTAL_POINTS.value] = total_bonus
            logging.info(f'Calculated attribute bonus {total_bonus} for "{bonus_key}"')
            self._total_attribute_bonuses[bonus_key] = tmp

        # flash(f'Calculated attribute bonuses', StatusCode.SUCCESS.value)
        return StatusCode.SUCCESS
    

    def _update_defense_bonus(self) -> StatusCode:
        total_defense = 0
        self._defense_bonus = {}

        # bonus from tribe
        defense = Tribe.get_properties(self.tribe).get(Armour.DEFENSE_BONUS, 0)
        total_defense += defense
        self._defense_bonus[self.tribe] = defense

        # bonus from profession
        defense = Profession.get_properties(self.profession).get(Armour.DEFENSE_BONUS, 0)
        total_defense += defense
        self._defense_bonus[self.profession] = defense

        # bonus from specialization
        defense = Specialization.get_properties(self.specialization).get(Armour.DEFENSE_BONUS, 0)
        total_defense += defense
        self._defense_bonus[self.specialization] = defense

        # bonus from weapons
        for weapon in self.equipped_weapons:
            defense = Weaponry.get_properties(weapon).get(Armour.DEFENSE_BONUS, 0)
            total_defense += defense
            self._defense_bonus[weapon] = defense

        # bonus from armour
        for armour in self.equipped_armour:
            defense = Armoury.get_properties(armour).get(Armour.DEFENSE_BONUS, 0)
            total_defense += defense
            self._defense_bonus[armour] = defense

        self._defense_bonus[Armour.DEFENSE_BONUS] = total_defense
        logging.info(f'Calculated defense bonus {total_defense}')
        # flash(f'Calculated defense bonus', StatusCode.SUCCESS.value)
        return StatusCode.SUCCESS
    

    def _update_max_hp(self) -> StatusCode:
        attribute_bonus = self.attribute_bonuses.get(AttributeKeys.ENDURANCE_BONUS, {}).get(AttributeKeys.ENDURANCE, 0)
        profession_hp = Profession.get_properties(self.profession).get(Statistics.HP, 0)

        self._max_hp = ( attribute_bonus + profession_hp ) * self.level

        logging.info(f'Updated max hp of character to {self.max_hp}')
        db.session.commit()
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


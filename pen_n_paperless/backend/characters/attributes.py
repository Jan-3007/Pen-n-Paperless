# character attributes class



# Python module imports
import logging
import typing

from flask import flash
from sqlalchemy import  Integer,\
                        ForeignKey,\
                        UniqueConstraint

from sqlalchemy.orm import  relationship,\
                            Mapped,\
                            mapped_column


# internal imports
from pen_n_paperless import db

from pen_n_paperless.config.character import CharacterConfig
from pen_n_paperless.common.keys import Attributes as key

# prevent cyclic import
if typing.TYPE_CHECKING:
    from .characters import Character




class Attributes(db.Model):
    """Class managing attributes and attribute bonuses

    The attribute bonus members only store the bonus that can be directly calculated from the attribute.

    """
    __tablename__ = "table_attributes"
    # __table_args__ = (UniqueConstraint("_character_id"),)

    _id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)

    # associate the character table in a one-to-one relationship
    _character_id: Mapped[int] = mapped_column(ForeignKey("table_characters._id"))
    _character: Mapped["Character"] = relationship("Character", back_populates='_attributes')


    # Members
    _endurance: Mapped[int] = mapped_column(Integer, default=0)
    _endurance_bonus: Mapped[int] = mapped_column(Integer, default=0)

    _strength: Mapped[int] = mapped_column(Integer, default=0)
    _strength_bonus: Mapped[int] = mapped_column(Integer, default=0)

    _dexterity: Mapped[int] = mapped_column(Integer, default=0)
    _dexterity_bonus: Mapped[int] = mapped_column(Integer, default=0)

    _intelligence: Mapped[int] = mapped_column(Integer, default=0)
    _intelligence_bonus: Mapped[int] = mapped_column(Integer, default=0)

    _charisma: Mapped[int] = mapped_column(Integer, default=0)
    _charisma_bonus: Mapped[int] = mapped_column(Integer, default=0)


    _total_points: Mapped[int] = mapped_column(Integer, default=CharacterConfig.total_attribute_points())
    _used_points: Mapped[int] = mapped_column(Integer, default=0)
    _remaining_points: Mapped[int] = mapped_column(Integer, default=0)



    def __init__(self):
        return
    
    def __str__(self) -> str:
        return ""
    


# -------------------------------------------------------------------------------

    # Properties
    @property
    def endurance(self) -> int:
        return self._endurance
    @property
    def endurance_bonus(self) -> int:
        return self._endurance_bonus

    @property
    def strength(self) -> int:
        return self._strength
    @property
    def strength_bonus(self) -> int:
        return self._strength_bonus

    @property
    def dexterity(self) -> int:
        return self._dexterity
    @property
    def dexterity_bonus(self) -> int:
        return self._dexterity_bonus

    @property
    def intelligence(self) -> int:
        return self._intelligence
    @property
    def intelligence_bonus(self) -> int:
        return self._intelligence_bonus

    @property
    def charisma(self) -> int:
        return self._charisma
    @property
    def charisma_bonus(self) -> int:
        return self._charisma_bonus

    @property
    def total_points(self) -> int:
        return self._total_points
    @property
    def used_points(self) -> int:
        return self._used_points
    @property
    def remaining_points(self) -> int:
        return self._remaining_points
    


# -------------------------------------------------------------------------------

    # public Methods
    # TODO maybe move to another content class, like tribe, profession and specialization
    @classmethod
    def get_name(cls, attr_key: key) -> str:
        match attr_key:
            case key.ENDURANCE: return "Endurance"
            case key.STRENGTH: return "Strength"
            case key.DEXTERITY: return "Dexterity"
            case key.INTELLIGENCE: return "Intelligence"
            case key.CHARISMA: return "Charisma"
            case _: return "Error"


    def get_attributes(self) -> dict:
        return {
            key.ENDURANCE: self.endurance,
            key.STRENGTH: self.strength,
            key.DEXTERITY: self.dexterity,
            key.INTELLIGENCE: self.intelligence,
            key.CHARISMA: self.charisma,
        }
    
    def get_attribute_bonuses(self) -> dict:
        # TODO with for loop and dict comprehension
        return {
            key.ENDURANCE_BONUS: self.endurance_bonus,
            key.STRENGTH_BONUS: self.strength_bonus,
            key.DEXTERITY_BONUS: self.dexterity_bonus,
            key.INTELLIGENCE_BONUS: self.intelligence_bonus,
            key.CHARISMA_BONUS: self.charisma_bonus,
        }
    
    def set_attribute(self, attribute_key: key, value: int) -> bool:
        """
        Update the value of the specified attribute
        
        :param self: Description
        :param key: Description
        :type key: key
        :param value: The absolute value to be set
        :type value: int
        :return: Description
        :rtype: bool
        """

        logging.debug(f'Updating attribute "{attribute_key}" to {value}')

        # get old value
        old_value = self.get_attributes().get(attribute_key, -1)
        if old_value < 0:
            logging.error(f'Failed to retrieve value from "{attribute_key}". Returned {old_value}')
            flash("Internal error", "error")
            return False

        # set new value
        success = self._update_attribute(attribute_key, value)
        if not success:
            return False

        # update points
        success = self._update_points()
        if not success:
            # revert changes
            self._update_attribute(attribute_key, old_value)
            return False
        
        success = self._update_attribute_bonus(attribute_key)
        if not success:
            return False
        
        db.session.commit()

        logging.debug(f'Updated attribute "{attribute_key}" to value {value}')
        flash("Update successful", "success")
        return True

    def modify_attribute(self, attribute_key: key, value: int) -> bool:
        """
        Update the value of the specified attribute
        
        :param self: Description
        :param key: Description
        :type key: key
        :param value: The relative value to be added
        :type value: int
        :return: Description
        :rtype: bool
        """

        if type(value) is not int:
            logging.error(f'"{value}" is not an integer. Cannot set for attribute {attribute_key}')
            return False

        # get old value
        old_value = self.get_attributes().get(attribute_key, -1)
        if old_value < 0:
            logging.error(f'Failed to retrieve value from "{attribute_key}". Returned {old_value}')
            flash("Internal error", "error")
            return False
        
        return self.set_attribute(attribute_key, old_value + value)


    def convert_key(self, original_key: key) -> key:

        bonus_extension = key.ATTRIBUTE_BONUS.value.removeprefix(key.ATTRIBUTE.value)

        if original_key == key.ATTRIBUTE:
            return key(original_key.value + bonus_extension)
        
        elif original_key == key.ATTRIBUTE_BONUS:
            return key(original_key.value.removesuffix(bonus_extension))

        else:
            logging.error(f'Failed to convert "{original_key}"')
            flash("Internal error", "error")
            return key.ATTRIBUTE
        
    
# -------------------------------------------------------------------------------

    # private Methods
    def _update_attribute(self, attribute_key: key, value: int) -> bool:
        """
        Update the attribute to the given value.
        
        :param self: Description
        :param attribute_key: Description
        :type attribute_key: key
        :param value: Description
        :type value: int
        :return: True if the update was successful.
        :rtype: bool
        """
        match attribute_key:
            case key.ENDURANCE:
                self._endurance = value
            case key.STRENGTH:
                self._strength = value
            case key.DEXTERITY:
                self._dexterity = value
            case key.INTELLIGENCE:
                self._intelligence = value
            case key.CHARISMA:
                self._charisma = value
            case _:
                logging.error(f'Tried to update an unknown attribute "{attribute_key}"')
                flash(f'Internal error', 'error')
                return False
            
        db.session.commit()
        return True


    def _update_points(self) -> bool:
        """
        Update the values of the used and remaining points.

        This method will fail if the remaining points would be less than 0.
        
        :param self: Description
        :return: True if the points have been updated.
        :rtype: bool
        """
        temp_used_points = (self.endurance + self.strength + self.dexterity + self.intelligence + self.charisma)
        temp_remaining_points = self.total_points - temp_used_points

        if temp_remaining_points >= 0:
            self._used_points = temp_used_points
            self._remaining_points = temp_remaining_points
            db.session.commit()
            return True
        
        logging.warning(f'User tried to use more points than were available.')
        flash("Not enough points available.", "error")
        return False



    def _update_attribute_bonus(self, attribute_key: key, initial_value: int = 0) -> bool:
        """
        Update the attribute bonus associated with the given attribute.
        
        :param self: Description
        :param attribute_key: Description
        :type attribute_key: key
        :return: True if the update was successful.
        :rtype: bool
        """
        
        attribute_value = self.get_attributes().get(attribute_key, -1)
        if attribute_value < 0:
            logging.error(f'Failed to retrieve value from "{attribute_key}". Returned {attribute_value}')
            flash("Internal error", "error")
            return False

        # determine bonus value
        bonus = initial_value

        if(attribute_value <= 1):
            bonus = -3
        elif(attribute_value == 2):
            bonus = -2
        elif(attribute_value == 3):
            bonus = -1
        elif(attribute_value in [4,5]):
            bonus = 0
        elif(attribute_value in [6,7]):
            bonus = 1
        elif(attribute_value in [8,9,10]):
            bonus = 2
        elif(attribute_value in [11,12,13,14]):
            bonus = 3
        elif(attribute_value in [15,16,17,18,19]):
            bonus = 4
        elif(attribute_value in [20,21,22,23,24,25]):
            bonus = 5
        elif(attribute_value > 25):
            bonus = 6

        # set new bonus value
        match attribute_key:
            case key.ENDURANCE:
                self._endurance_bonus = bonus
            case key.STRENGTH:
                self._strength_bonus = bonus
            case key.DEXTERITY:
                self._dexterity_bonus = bonus
            case key.INTELLIGENCE:
                self._intelligence_bonus = bonus
            case key.CHARISMA:
                self._charisma_bonus = bonus
            case _:
                logging.error(f'Tried to update an unknown attribute bonus for the attribute "{attribute_key}"')
                flash(f'Internal error', 'error')
                return False
            
        db.session.commit()
        return True
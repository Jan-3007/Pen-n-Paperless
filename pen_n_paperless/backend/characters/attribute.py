# character attributes class



# Python module imports
import logging

from flask import flash
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


# internal imports
from pen_n_paperless import db

from pen_n_paperless.config.character import CharacterConfig
from pen_n_paperless.common.keys import Attributes as key



class Attributes():
    __tablename__ = "table_attributes"

    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # associate the character table in a one-to-one relationship
    _character_id = db.Column(db.Integer, ForeignKey("table_characters._id"))
    _character = relationship(
        'Character',
        back_populates='_attributes'
    )


    # Members
    _endurance = db.Column(db.Integer, default=0)
    _endurance_bonus = db.Column(db.Integer, default=0)

    _strength = db.Column(db.Integer, default=0)
    _strength_bonus = db.Column(db.Integer, default=0)

    _dexterity = db.Column(db.Integer, default=0)
    _dexterity_bonus = db.Column(db.Integer, default=0)

    _intelligence = db.Column(db.Integer, default=0)
    _intelligence_bonus = db.Column(db.Integer, default=0)

    _charisma = db.Column(db.Integer, default=0)
    _charisma_bonus = db.Column(db.Integer, default=0)


    _total_points = db.Column(db.Integer, default=CharacterConfig.total_attribute_points())
    _used_points = db.Column(db.Integer, default=0)
    _remaining_points = db.Column(db.Integer, default=0)



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
    def get_attributes(self) -> dict:
        return {
            key.ENDURANCE: self.endurance,
            key.STRENGTH: self.strength,
            key.DEXTERITY: self.dexterity,
            key.INTELLIGENCE: self.intelligence,
            key.CHARISMA: self.charisma,
        }
    
    def get_attribute_bonuses(self) -> dict:
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
        :param value: Description
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



    def _update_attribute_bonus(self, attribute_key: key) -> bool:
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
        bonus = 0

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

        return True
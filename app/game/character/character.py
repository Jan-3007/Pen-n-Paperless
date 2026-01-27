from ... import db
from flask import flash

from typing import List
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship, Mapped, mapped_column


from ...strings import Strings, Messages
from .history import XPHistory, HPHistory

from ...game_settings import GameSettings
from ..tribe import Tribe
from ..profession import Profession
from ..specialization import Specialization
from ..armoury import Armoury
from ..weaponry import Weaponry
from ..abilities import Abilities



class Character(db.Model):
    __tablename__ = "character_table"


    # database connections
    _id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)

    # One to Many relationships for XP and HP history
    _new_xp_history: Mapped[List[XPHistory]] = relationship(back_populates="_character")
    _new_hp_history: Mapped[List[HPHistory]] = relationship(back_populates="_character")


    def __init__(self, name):
        self._name = name
        self._equipped_armour = ["Empty" for i in range(0, GameSettings.max_armour_sets())]
        self._equipped_weapons = ["Empty" for i in range(0, GameSettings.max_number_of_weapons())]


    # _id = db.Column(db.Integer, primary_key=True)

    # Definition of Character properties
    _name = db.Column(db.String(100), default="")

    # Tribe, Profession and Specialization instances
    _tribe = db.Column(db.String(100), default="")
    _profession = db.Column(db.String(100), default="")
    _specialization = db.Column(db.String(100), default="")

    # Statistics
    _level = db.Column(db.Integer, default=1)
    _experience = db.Column(db.Integer, default=0)
    _max_hp = db.Column(db.Integer, default=10)
    _current_hp = db.Column(db.Integer, default=10)

    # Attributes
    _remaining_attribute_points = db.Column(db.Integer, default=0)
    _used_attribute_points = db.Column(db.Integer, default=0)

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

    # Abilities
    _max_ability_points = db.Column(db.Integer, default=0)
    _remaining_ability_points = db.Column(db.Integer, default=0)
    _developed_abilities = db.Column(MutableDict.as_mutable(db.PickleType), default=dict)
    '''
    ability key:
    {
        current level : ability level,
        cost history : [int],
    }
    '''

    # Armor
    _defense_bonus = db.Column(db.Integer, default=0)
    _equipped_armour = db.Column(MutableList.as_mutable(db.PickleType), default=list)

    # Weapons
    _equipped_weapons = db.Column(MutableList.as_mutable(db.PickleType), default=list)

    # Inventory
    _inventory = db.Column(db.Text, default='')

    # HP history
    # _hp_history_entry = HistoryEntry()
    # _hp_history = db.Column(MutableList.as_mutable(db.PickleType), default=list)

    # XP history
    # _xp_history_entry = HistoryEntry()
    # _xp_history = db.Column(MutableList.as_mutable(db.PickleType), default=list)

    # Notes
    _notes = db.Column(db.Text, default='')







    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, character_name: str):
        self._name = character_name
        db.session.commit()
        return


    @property
    def tribe(self):
        """returns the tribe key"""
        return self._tribe
    @tribe.setter
    def tribe(self, tribe_name: str):
        """sets the tribe key"""
        self._tribe = tribe_name
        # influences attribute_bonuses and defense_bonus
        self._update_attribute_bonuses()
        self._update_defense_bonus()
        db.session.commit()

    
    @property
    def profession(self):
        """returns the profession key"""
        return self._profession
    @profession.setter
    def profession(self, profession_name: str):
        """sets the profession key"""
        self._profession = profession_name
        self._update_attribute_bonuses()
        self._update_max_hp()
        self._update_defense_bonus()
        db.session.commit()


    @property
    def specialization(self):
        """returns the specialization key"""
        return self._specialization
    @specialization.setter
    def specialization(self, specialization_name: str):
        """sets the specialization key"""
        self._specialization = specialization_name
        self._update_attribute_bonuses()
        self._update_defense_bonus()
        db.session.commit()


    @property
    def level(self):
        return self._level

    @property
    def experience(self):
        return self._experience


    @property
    def max_hp(self):
        return self._max_hp
    
    # @property
    def properties(self):
        return {
            Strings.id.value: self._id,
            Strings.names.value: self._name,
            Strings.tribe.value: self._tribe,
            Strings.profession.value: self._profession,
            Strings.specialization.value: self._specialization,
        }
    
    # @property
    def statistics(self):
        return {
            Strings.Statistics.level.value: self._level,
            Strings.Statistics.experience.value: self._experience,
            Strings.Statistics.hp.value: self._current_hp,
            Strings.Statistics.max_hp.value: self._max_hp,
        }

    # @property
    def attributes(self) -> dict:
        return {
            Strings.Attributes.endurance.value: self._endurance,
            Strings.Attributes.strength.value: self._strength,
            Strings.Attributes.dexterity.value: self._dexterity,
            Strings.Attributes.intelligence.value: self._intelligence,
            Strings.Attributes.charisma.value: self._charisma,
            Strings.Attributes.used_attribute_points.value: self._used_attribute_points,
            Strings.Attributes.remaining_attribute_points.value: self._remaining_attribute_points
        }

    # @property
    def attribute_bonuses(self):
        return {
            Strings.Attributes.endurance_bonus.value: self._endurance_bonus,
            Strings.Attributes.strength_bonus.value: self._strength_bonus,
            Strings.Attributes.dexterity_bonus.value: self._dexterity_bonus,
            Strings.Attributes.intelligence_bonus.value: self._intelligence_bonus,
            Strings.Attributes.charisma_bonus.value: self._charisma_bonus,
        }

    @property
    def notes(self):
        return self._notes
    
    @property
    def defense_bonus(self):
        return self._defense_bonus
    
    @property
    def armour(self) -> list:
        return self._equipped_armour
    
    @property
    def weapons(self):
        return self._equipped_weapons
    
    
    @property
    def inventory(self):
        return self._inventory


    @property
    def max_ability_points(self):
        return self._max_ability_points

    @property
    def remaining_ability_points(self):
        return self._remaining_ability_points

    @property
    def hp_history(self):
        return self._new_hp_history

    @property
    def xp_history(self):
        return self._new_xp_history

    @property
    def abilities(self):
        return self._developed_abilities




# methods

    # Convert Character to json-serializable dictionary
    def to_json(self):
        return {
            Strings.properties.value: self.properties,
            Strings.Statistics.statistics.value: self.statistics,
            Strings.Attributes.attributes.value: self.attributes,
            Strings.Attributes.attribute_bonuses.value: self.attribute_bonuses,
            Strings.notes.value: self._notes,
            Strings.Armour.equipped_armour.value: self._equipped_armour,
            Strings.equipped_weapons.value: self._weapons,
            Strings.inventory.value: self._inventory,
            Strings.hp_history.value: self.hp_history,
            Strings.xp_history.value: self.xp_history,
       }


    def initialize(self):

        self._update_attribute_bonuses()
        self._update_current_hp()
        self._update_max_ability_points()






    # Update attribute value, check remaining points, calculate bonus, and commit changes
    # returns True if successful, False otherwise
    def set_attribute(self, attribute: str, value: int) -> bool:

        print(attribute)
        print(value)

        # get old value 
        old_value = self.attributes().get(attribute)

        # set new value
        self._update_attribute(attribute, value)

        remaining_points = self._update_remaining_attribute_points()
        if(remaining_points < 0):
            # revert change
            self._update_attribute(attribute, old_value)
            # show error
            flash(f'{Messages.error_missing_attribute_points()}', 'error')
            return False
        else:
            # got enough points left (0 or more remaining), calculate bonus and confirm
            self._update_attribute_bonuses()
            self._update_max_hp()

            flash(f'{attribute} {Messages.updated_successfully()}', 'success')
            db.session.commit()

        return True

    def _update_attribute(self, attribute: str, value: int):
        match attribute:
            case Strings.Attributes.endurance.value:
                self._endurance = value
            case Strings.Attributes.strength.value:
                self._strength = value
            case Strings.Attributes.dexterity.value:
                self._dexterity = value
            case Strings.Attributes.intelligence.value:
                self._intelligence = value
            case Strings.Attributes.charisma.value:
                self._charisma = value
            case _:
                flash(f'{Messages.error_unknown_attribute()}{attribute}', 'error')
                return False
        db.session.commit()
        return True

    def _update_attribute_bonuses(self) -> bool:
        for bonus in self.attribute_bonuses().keys():
            new_bonus = 0
    
            # bonus from attribute
            new_bonus += self._calculate_base_attribute_bonus(bonus.replace('_bonus',''))
            # bonus from tribe
            new_bonus += Tribe.get_properties(self._tribe).get(bonus, 0)
            # bonus from profession
            new_bonus += Profession.get_properties(self._profession).get(bonus, 0)
            # bonus from specialization
            new_bonus += Specialization.attribute_bonus(self._specialization, bonus, self._level)
            # bonus from weapons
            for weapon in self._equipped_weapons:
                new_bonus += Weaponry.get_properties(weapon).get(bonus, 0)
            # bonus from armor
            for armour in self._equipped_armour:
                new_bonus += Armoury.get_properties(armour).get(bonus, 0)
            # no bonus from abilities
            # for ability_key in self._developed_abilities.keys():
                # new_bonus += Abilities.get_properties(ability_key).get(bonus, 0)
            # no bonus from inventory items

            # flash(f'{self._tribe}{new_bonus}', 'success')

            # set new bonus value
            match bonus:
                case Strings.Attributes.endurance_bonus.value:
                    self._endurance_bonus = new_bonus
                case Strings.Attributes.strength_bonus.value:
                    self._strength_bonus = new_bonus
                case Strings.Attributes.dexterity_bonus.value:
                    self._dexterity_bonus = new_bonus
                case Strings.Attributes.intelligence_bonus.value:
                    self._intelligence_bonus = new_bonus
                case Strings.Attributes.charisma_bonus.value:
                    self._charisma_bonus = new_bonus
                case _:
                    flash(f'{Messages.error_unknown_attribute()}{bonus}', 'error')
                    return False

        self._update_max_ability_points()

        flash(f'{Messages.bonuses_updated_successfully()}', 'success')
        db.session.commit()
        return True


    def _calculate_base_attribute_bonus(self, attribute: str) -> int: 

        match attribute:
            case Strings.Attributes.endurance.value:
                attribute_value = self._endurance
            case Strings.Attributes.strength.value:
                attribute_value = self._strength
            case Strings.Attributes.dexterity.value:
                attribute_value = self._dexterity
            case Strings.Attributes.intelligence.value:
                attribute_value = self._intelligence
            case Strings.Attributes.charisma.value:
                attribute_value = self._charisma

        bonus = 0
        if(attribute_value == 1):
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

        return bonus
    

    # Update total attribute points and return remaining points
    def _update_remaining_attribute_points(self) -> int:
        used_points = (self._endurance + self._strength + self._dexterity + self._intelligence + self._charisma)
        remaining = GameSettings.total_attribute_points() - used_points

        if remaining >= 0:
            self._used_attribute_points = used_points
            self._remaining_attribute_points = remaining
            db.session.commit()
        
        return remaining
        


    def _update_max_hp(self) -> int:
        # TODO error: when no max_hp in profession, use max_hp of specialization
        hp = ( self.attribute_bonuses().get(Strings.Attributes.endurance_bonus.value)
              + Profession.get_properties(self._profession).get(Strings.Statistics.max_hp.value, 0)
              ) * self._level

        self._max_hp = hp

        self._update_current_hp()
        db.session.commit()
        return


    def _update_level(self):
        xp = self._experience
        old_level = self._level

        if xp < 1000:
            level = 1
        elif xp < 2000:
            level = 2
        elif xp < 3000:
            level = 3
        elif xp < 5000:
            level = 4
        elif xp < 7500:
            level = 5
        elif xp < 10000:
            level = 6
        elif xp < 12500:
            level = 7
        elif xp < 15000:
            level = 8
        elif xp < 17500:
            level = 9
        else:
            level = 10

        self._level = level

        if level != old_level:
            self._update_max_hp()
            self._update_max_ability_points()

        db.session.commit()
        return





    def _update_max_ability_points(self):
        base_points = 8 + self._intelligence_bonus

        self._max_ability_points = base_points * self._level

        db.session.commit()

        self._update_remaining_ability_points()

        return
    

    def _update_remaining_ability_points(self):
        used_points = 0

        for ability in self._developed_abilities.values():
            cost_list = ability.get(Strings.Abilities.cost_history.value, [])

            for cost in cost_list:
                used_points += cost

        self._remaining_ability_points = self._max_ability_points - used_points

        print(f"Updated remaining ability points: {self._remaining_ability_points}")

        db.session.commit()
        return
    

    def update_abilities(self, ability_key: str, delta: int) -> bool:
        """Update the level of a certain ability by delta (can be negative).

        Returns True if successful, False otherwise.
        """

        # check if delta is greater than 0
        if delta > 0:
            # upgrade ability
            # print(f"Upgrading ability {ability_key} by {delta}")

            # check if enough ability points are remaining
            # delta equals number of levels to upgrade
            if Abilities.get_cost(ability_key, self._profession)[delta-1] > self._remaining_ability_points:
                print(f"Not enough ability points to upgrade {ability_key}")
                flash(f'Not enough ability points to upgrade {ability_key}', 'error')
                return True
            
            # check if ability does not already exists
            if ability_key not in self._developed_abilities:
                self._add_ability(ability_key, delta)
                flash(f'Ability {ability_key} added.', 'success')

            # enough points and ability exists, update it
            else:
                self._update_ability(ability_key, delta)
                flash(f'Ability {ability_key} upgraded.', 'success')

            db.session.commit()

        elif delta < 0:
            # downgrade/remove ability
            print(f"Downgrading ability {ability_key} by {delta}")

            # check if ability does not already exist
            if ability_key not in self._developed_abilities:
                flash(f'Ability {ability_key} not developed.', 'success')
                return True
            
            else:
                self._update_ability(ability_key, delta)
                flash(f'Ability {ability_key} downgraded.', 'success')
            
            db.session.commit()

        else:
            # no change
            flash(f'No change to ability {ability_key}', 'success')
            return True


        self._update_remaining_ability_points()
        self._update_attribute_bonuses()
        db.session.commit()
        return True




    def _add_ability(self, ability_key: str, level: int):
        cost = Abilities.get_cost(ability_key, self._profession)[level-1]
        self._developed_abilities[ability_key] = {
            Strings.Abilities.level.value: level,
            Strings.Abilities.cost_history.value: [cost]
        }
        print(f"Ability {self._developed_abilities.get(ability_key)} added")
        db.session.commit()
        return


    def _update_ability(self, ability_key: str, delta: int):
        current_level = self._developed_abilities.get(ability_key, {}).get(Strings.Abilities.level.value, 0)
        new_level = current_level + delta

        # check if new level is less than or equal to 0
        if new_level <= 0:
            # remove ability
            self._developed_abilities.pop(ability_key)
            print(f"Ability {ability_key} removed")
            flash(f'Ability {ability_key} removed.', 'success')

        else:
            # calculate cost for level change
            cost = Abilities.get_cost(ability_key, self._profession)[abs(delta) -1]
            # print(f"Ability {ability_key} updated to level {new_level} with cost {cost}")

            # update ability entry
            # get current entry
            old_entry = self._developed_abilities.get(ability_key, {})
            # print(f"Old entry: {old_entry}")

            # set new level and append cost to cost history
            old_cost_history = old_entry.get(Strings.Abilities.cost_history.value, [])
            # print(f"Old cost history: {old_cost_history}")
            # print(f"Cost to append: {cost if delta > 0 else (-cost)}")

            new_cost_history = old_cost_history + [cost if delta > 0 else (-cost)]
            # print(f"New cost history: {new_cost_history}")

            new_entry = {
                Strings.Abilities.level.value: new_level,
                Strings.Abilities.cost_history.value: new_cost_history
            }
            # print(f"New entry: {new_entry}")

            self._developed_abilities[ability_key] = new_entry


        db.session.commit()

        return




    def _update_defense_bonus(self):
        total_defense = 0
        # no bonus from attribute

        # bonus from tribe
        total_defense += Tribe.get_properties(self._tribe).get(Strings.Armour.defense_bonus.value, 0)
        # bonus from profession
        total_defense += Profession.get_properties(self._profession).get(Strings.Armour.defense_bonus.value, 0)
        # bonus from specialization
        total_defense += Specialization.get_properties(self.specialization).get(Strings.Armour.defense_bonus.value, 0)
        # bonus from weapons
        for weapon in self._equipped_weapons:
            total_defense += Weaponry.get_properties(weapon).get(Strings.Armour.defense_bonus.value, 0)
        # bonus from armour
        for armour in self._equipped_armour:
            props = Armoury.get_properties(armour)
            total_defense += props.get(Strings.Armour.defense_bonus.value, 0)

        # no bonus from inventory items

        self._defense_bonus = total_defense
        db.session.commit()
        return


    # set armour to one of Strings.Armour
    def select_armour(self, armour_type : str, pos : int) -> bool:
        """Sets the equipped armour of the character, returns false on error"""

        # first, let's check if any armour is even allowed
        if GameSettings.max_armour_sets() <= 0:
            flash('No armour allowed', 'error')
            return True
        
        # check if pos is actually within the range of allowed number of armour sets
        if not 0 <= pos < GameSettings.max_armour_sets():
            flash('Internal error, armour pos not allowed', 'error')
            return False


        # check if given armour type is valid and if given position can exist
        if armour_type in Strings.Armour:

            self._equipped_armour[pos] = armour_type

            flash(Armoury.get_properties(armour_type).get(Strings.names.value)[GameSettings.language()] + ' equipped', 'success')
            db.session.commit()

            # update all dependent properties
            self._update_attribute_bonuses()
            self._update_defense_bonus()

            db.session.commit()
            return True

        else:
            return False


    # set armour to one of Strings.Armour
    def select_weapon(self, weapon_type : str, pos : int) -> bool:
        """Sets the equipped armour of the character, returns false on error"""

        # first, let's check if any armour is even allowed
        if GameSettings.max_number_of_weapons() <= 0:
            flash('No weapons allowed', 'error')
            return True
        
        # check if pos is actually within the range of allowed number of armour sets
        if not 0 <= pos < GameSettings.max_number_of_weapons():
            flash('Internal error, weapon pos not allowed', 'error')
            return False

        # check if given armour type is valid and if given position can exist
        if weapon_type in Strings.Weapons:

            self._equipped_weapons[pos] = weapon_type
            db.session.commit()

            # update all dependent properties
            self._update_attribute_bonuses()
            self._update_defense_bonus()

            flash(Weaponry.get_properties(weapon_type).get(Strings.names.value)[GameSettings.language()] + ' equipped', 'success')

            db.session.commit()
            return True

        else:
            return False




    def _add_xp_history_entry(self, value: int, description: str):

        new_db_entry = XPHistory(value=value, description=description)
        self._new_xp_history.append(new_db_entry)
    

        db.session.commit()

        self._update_experience()
        flash('New XP history entry added', 'success')
        db.session.commit()
        return

    def _remove_xp_history_entry(self, entry_nb: int) -> bool:
        # check if entry exists and try to remove it if found
        for xp in self._new_xp_history:
            try:
                if xp.get_properties().get(Strings.entry_number.value) == entry_nb:
                    self._new_xp_history.remove(xp)
            except:
                return False   

        db.session.commit()

        self._update_experience()
        flash(f'Entry removed from XP history', 'success')
        db.session.commit()
        return True




    def _add_hp_history_entry(self, value: int, description: str):

        new_db_entry = HPHistory(value=value, description=description)
        self._new_hp_history.append(new_db_entry)


        db.session.commit()

        self._update_current_hp()
        flash('New HP history entry added', 'success')
        db.session.commit()
        return

    def _remove_hp_history_entry(self, entry_nb: int) -> bool:
        # check if entry exists and try to remove it if found
        for hp in self._new_hp_history:
            try:
                if hp.get_properties().get(Strings.entry_number.value) == entry_nb:
                    self._new_hp_history.remove(hp)
            except:
                return False 

        db.session.commit()

        self._update_current_hp()
        flash(f'Entry removed from HP history', 'success')
        db.session.commit()
        return True



    def _update_current_hp(self):

        hp = self._max_hp

        for entry in self._new_hp_history:
            # stored value has to be negative in order to be interpreted as damage
            hp += int(entry.get_properties().get(Strings.val.value, 0))

        if hp <= 0:
            hp = 0
            flash('Health critical', 'error')

        print(f"New HP: {hp}")
        self._current_hp = hp

        db.session.commit()
        return


    def _update_experience(self):

        xp = 0

        print(self._new_xp_history)

        for entry in self._new_xp_history:

            val = entry.get_properties().get(Strings.val.value, "")
            print(f"{type(val)}: {val}")
            
            if val:
                xp += int(val)
            else:
                xp += 0

        self._experience = xp

        self._update_level()
        db.session.commit()
        return




    def update(self, key, data: dict) -> bool:  # TODO cleanup return values
        """main character properties update method, returns False on error"""

        if not Strings.val.value in data:
            flash('Missing a value in data', 'error')
            return False


        value = data.get(Strings.val.value, None)
        delta = data.get(Strings.Abilities.delta.value, None)


        # allow list values for multi-select fields (e.g., armour) TODO only cast and strip() neede?
        if not isinstance(value, list):
            try:
                value = str(value).strip()
            except Exception:
                pass


        # handle armour updates (single or multiple selections)
        # armour_key = None
        # try:
        #     armour_key = Strings.Armour.armour.value
        # except Exception:
        #     armour_key = 'armour'

        if key == Strings.Armour.armour.value:
            if value.find("-") >= 0:
                
                value_list = value.split("-")

                self.select_armour(value_list[1], int(value_list[0].strip()))
                db.session.commit()
                return True

            else:
                flash(f'Invalid syntax for armour selection', 'error')
                return False


        if key == Strings.Weapons.weapons.value:
            if value.find("-") >= 0:
                
                value_list = value.split("-")

                self.select_weapon(value_list[1], int(value_list[0].strip()))
                db.session.commit()
                return True

            else:
                flash(f'Invalid syntax for armour selection', 'error')
                return False



        # statistics are read-only

        if key in Strings.Attributes:
            return self.set_attribute(key, value)

        if key in Strings.Abilities:
            # print(f"Starting update of {key}")
            if self._profession == "":
                flash('Set profession before updating abilities', 'error')
                return True
            
            return self.update_abilities(key, delta)


        description = None
        if Strings.description.value in data:
            description = data.get(Strings.description.value, "").strip()


        match key:
            case Strings.names.value:
                self._name = value
            
            case Strings.tribe.value:
                tribe_key = value

                self._tribe = tribe_key
                db.session.commit()
                self._update_attribute_bonuses()
                self._update_defense_bonus()

            case Strings.profession.value:
                profession_key = value

                self._profession = profession_key
                db.session.commit()
                self._update_max_hp()
                self._update_attribute_bonuses()
                self._update_defense_bonus()

                # delete specialization when profession is changed
                self._specialization = ""

            case Strings.specialization.value:
                specialization_key = value

                self._specialization = specialization_key
                db.session.commit()
                self._update_attribute_bonuses()
                self._update_defense_bonus()

            case Strings.notes.value:
                self._notes = value

            case Strings.xp_history.value:
                if description != None:
                    self._add_xp_history_entry(value=value, description=description)
                else:
                    self._remove_xp_history_entry(entry_nb=int(value))

            case Strings.hp_history.value:
                if description != None:
                    self._add_hp_history_entry(value=value, description=description)
                else:
                    self._remove_hp_history_entry(entry_nb=int(value))


                # TODO Strings.inventory

            case _:
                return False


        db.session.commit()
        return True






def get_by_name(ch_name):
    return Character.query.filter_by(_name=ch_name).first()


def create_character(name):
    c = Character(name=name)
    db.session.add(c)
    db.session.commit()
    c.initialize()
    return c

# TODO not working
# returns True if successful, False otherwise
def delete_character(char_id) -> bool:
    c = Character.query.get(char_id)
    if c:
        db.session.delete(c)
        db.session.commit()
        return True
    return False



# TODO
def export_character(char_id):
    c = Character.query.get(char_id)
    if c:
        return c.to_json()
    return None





# Python module imports
from enum import Enum, auto


# Base class with modified methods for all enums
class Key(Enum):
    # Implementing these methods allows for calling Key.member instead of Key.member.value
    def __str__(self) -> str:
        return str(self.value)
    # def __repr__(self):
    #     return str(self.value)
    
    # Change the functionality of the auto method
    #   the value will be the name in lowercase as a atring
    @staticmethod
    def _generate_next_value_(name, start, count, last_values) -> str:
        return str(name).lower()
    
    def __getitem__(self, index: str):
        return self.__getitem__(index.upper())
    
    

def get_enum_values(enum_class):
    """
    Helper method in order to be able to use enums in the database
    
    :param enum_class: Description
    """
    return [member.value for member in enum_class]





# Generic keys
class Generic(Key):
    ID = auto()
    NAME = auto()
    VALUE = auto()
    PROPERTIES = auto()
    DESCRIPTION = auto()

    CATEGORY = auto()
    NOTES = auto()
    COST = auto()
    WEIGHT = auto()
    NONE = auto()

    TOTAL_POINTS = auto()
    USED_POINTS = auto()
    REMAINING_POINTS = auto()

    
# Statistics keys
class Statistics(Key):
    STATISTICS = auto()
    LEVEL = auto()
    EXPERIENCE = auto()
    HP = auto()
    CURRENT_HP = auto()
    MAX_HP = auto()


# Attribute keys
class Attributes(Key):
    ATTRIBUTE = auto()
    ATTRIBUTE_BONUS = auto()

    ENDURANCE = auto()
    ENDURANCE_BONUS = auto()
    STRENGTH = auto()
    STRENGTH_BONUS = auto()
    DEXTERITY = auto()
    DEXTERITY_BONUS = auto()
    INTELLIGENCE = auto()
    INTELLIGENCE_BONUS = auto()
    CHARISMA = auto()
    CHARISMA_BONUS = auto()


# Armour keys
class Armour(Key):
    ARMOUR = auto()
    DEFENSE_BONUS = auto()
    EQUIPPED_ARMOUR = auto()

    WOOL = auto()
    LEATHER = auto()
    CHAINMAIL = auto()
    COMPOSITE = auto()
    PLATE = auto()


# Weapon keys
class Weapons(Key):
    WEAPON = auto()
    ATTACK_BONUS = auto()
    EQUIPPED_WEAPONS = auto()
    INI_BONUS = auto()

    LONGSWORD = auto()
    DAGGER = auto()
    TWO_HANDED_SWORD = auto()
    FALCATA = auto()
    EPEE = auto()
    CUTLAS = auto()
    DAMASCENE_BLADE = auto()
    CLAYMORE = auto()
    HATCHET = auto()
    BATTLEAXE = auto()
    THROWING_AXE = auto()
    JAVELIN = auto()
    LANCE = auto()
    PIKE = auto()
    HALBERD = auto()
    STAFF = auto()
    SHORTBOW = auto()
    LONGBOW = auto()
    COMPOSITE_BOW = auto()
    ROUND_SHIELD = auto()


# History keys
class History(Key):
    XP_HISTORY = auto()
    HP_HISTORY = auto()
    ENTRY_NUMBER = auto()
    TIMESTAMP = auto()


# Ability keys
class Abilities(Key):
    ABILITY = auto()
    MAX_ABILITY_POINTS = auto()
    REMAINING_ABILITY_POINTS = auto()

    ACROBATICS = auto()
    SNEAKING = auto()


# Tribe keys
class Tribes(Key):
    TRIBE = auto()

    ELF = auto()
    GNOME = auto()
    HALFELF = auto()
    HALFLING = auto()
    HALFORC = auto()
    HUMAN = auto()
    DWARF = auto()






# Profession keys
class Professions(Key):
    PROFESSION =auto()
    
    BARD = auto()
    THIEF = auto()
    HERBALIST = auto()
    WARRIOR = auto()
    RANGER = auto()
    SCIENTIST = auto()


# Spoecialization keys
class Specializations(Key):
    SPECIALIZATION = auto()
    EVOLUTION = auto()

    # Bard
    SPY = auto()
    ARTIST = auto()
    # Thief
    PICKPOCKET = auto()
    ASSASSIN = auto()
    # Herbalis
    CHEMIST = auto()
    HEALER = auto()
    # Warrior
    BERSERKER = auto()
    BOXER = auto()
    SOLDIER = auto()
    GUARD = auto()
    # Ranger
    SCOUT = auto()
    BEASTMASTER = auto()
    # Scientist
    ALCHEMIST = auto()
    GEOLOGIST = auto()
    MATHEMATICIAN = auto()
    PHARMACIST = auto()


# Character traits keys
class Traits(Key):
    TRAIT = auto()

    # Pickpocket - level 2
    IMPERSONATOR = auto()
    LOCKSMITH = auto()
    TRAP_DIFFUSER = auto()
    #            - level 4
    STREET_SMARTS = auto()
    SMUGGLER = auto()
    FENCE_CONTACTS = auto()

    # Assassin - level 2
    NIGHTVISION = auto()
    MINDCONTROL = auto()
    HIDDEN_BLADE = auto()



class Avatars(Key):
    AVATAR = auto()
    UPLOAD = auto()
    DELETE = auto()
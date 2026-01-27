from enum import Enum
from .game_settings import GameSettings as rules





# Define string constants to reduce hardcoding and potential typos
class Strings(Enum):

    # language-independent strings
    # properties
    properties = "properties"
    id = "id"
    names = "name"
    tribe = "tribe"
    profession = "profession"
    specialization = "specialization"

    # statistics
    class Statistics(Enum):
        statistics = "statistics"
        level = "level"
        experience = "experience"
        hp = "current_hp"
        max_hp = "max_hp"

    # attributes
    class Attributes(Enum):
        attributes = "attributes"
        remaining_attribute_points = "remaining_attribute_points"
        used_attribute_points = "used_attribute_points"
        endurance = "endurance"
        strength = "strength"
        dexterity = "dexterity"
        intelligence = "intelligence"
        charisma = "charisma"

        # attribute bonuses
        attribute_bonuses = "attribute_bonuses"
        endurance_bonus = "endurance_bonus"
        strength_bonus = "strength_bonus"
        dexterity_bonus = "dexterity_bonus"
        intelligence_bonus = "intelligence_bonus" 
        charisma_bonus = "charisma_bonus"



    weight = "weight"

    # armour
    class Armour(Enum):
        armour = "armour"
        defense_bonus = "defense_bonus"

        equipped_armour = "equipped_armour"
        wool = "wool"
        leather = "leather"
        chainmail  = "chainmail"
        composite = "composite"
        plate = "plate"


    # weapons
    class Weapons(Enum):
        weapons = "weapons"
        equipped_weapons = "equipped_weapons"
        attack_bonus = "attack_bonus"
        ini_bonus = "ini_bonus"

        longsword = "longsword"
        dagger = "dagger"
        two_handed_sword = "two_handed_sword"
        falcata = "falcata"
        epee = "epee"
        cutlas = "cutlas"
        damascene_blade = "damascene_blade"
        claymore = "claymore"
        hatchet = "hatchet"
        battleaxe = "battleaxe"
        throwing_axe = "throwing_axe"
        javelin = "javelin"
        lance = "lance"
        pike = "pike"
        halberd = "halberd"
        staff = "staff"
        shortbow = "shortbow"
        longbow = "longbow"
        composite_bow = "composite_bow"
        round_shield = "round_shield"


    # inventory
    inventory = "inventory"
    quantity = "quantity"

    # history
    xp_history = "xp_history"
    hp_history = "hp_history"
    entry_number = "entry_number"
    val = "value"
    timestamp = "timestamp"

    # other
    notes = "notes"
    description = "description"

    class Tribes(Enum):
        """language-independent"""
        elf = "elf"
        gnome = "gnome"
        halfelf = "halfelf"
        halfling = "halfling"
        halforc = "halforc"
        human = "human"
        dwarf = "dwarf"

    class Professions(Enum):
        """language-independent"""
        bard = "bard"
        thief = "thief"
        herbalist = "herbalist"
        warrior = "warrior"
        ranger = "ranger"
        scientist = "scientist"

    class Specialization(Enum):
        """language-independent"""
        spy = "spy"
        artist = "artist"
        pickpocket = "pickpocket"
        assassin = "assassin"
        chemist = "chemist"
        healer = "healer"
        berserker = "berserker"
        boxer = "boxer"
        soldier = "soldier"
        guard = "guard"
        scout = "scout"
        beastmaster = "beastmaster"
        alchemist = "alchemist"
        geologist = "geologist"
        mathematician = "mathematician"
        pharmacist = "pharmacist"

        evolution = "evolution"
        required_level = "required_level"


    class Abilities(Enum):
        """language-independent"""
        abilities = "abilities"
        cost = "cost"
        cost_history = "cost_history"
        max_ability_points = "max_ability_points"
        remaining_ability_points = "remaining_ability_points"
        level = "level"
        delta = "delta"
        max_upgrades_per_level = "max_upgrades_per_level"
        

        nightvision = "nightvision"
        mindcontrol = "mindcontrol"
        hidden_blade = "hidden_blade"
        acrobatics = "acrobatics"
        sneaking = "sneaking"
        impersonator = "impersonator"
        locksmith = "locksmith"
        trap_difuser = "trap_difuser"
        street_smarts = "street_smarts"
        smuggler = "smuggler"
        fence_contacts = "fence_contacts"
        athletics = "athletics"
        intimidation = "intimidation"
        poison_mixing = "poison_mixing"
        healing = "healing"
        inspiration = "inspiration"
        culture = "culture"
        art = "art"
        cunning = "cunning"
        medicine = "medicine"
        nature = "nature"
        riding = "riding"
        swimming = "swimming"
        animal_care = "animal_care"
        survival = "survival"
        conviction = "conviction"
        investigation = "investigation"
        weapons1 = "weapons1"
        weapons2 = "weapons2"
        weapons3 = "weapons3"
        perception = "perception"
        knowledge = "knowledge"





# language-dependent strings
class Messages():
    """language-dependent"""
    _error_missing_attribute_points = [ "Not enough attribute points available", "Nicht genügend Attributspunkte verfügbar" ]
    _error_unknown_attribute = [ "Unknown attribute: ", "Unbekanntes Attribut: " ]


    _updated_successfully = [ "updated successfully", "erfolgreich aktualisiert" ] 
    _bonuses_updated_successfully = [ "Bonuses updated successfully", "Bonusse erfolgreich aktualisiert" ]




    @classmethod
    def error_missing_attribute_points(cls):
        return cls._error_missing_attribute_points[rules.language()]
    
    @classmethod
    def updated_successfully(cls):
        return cls._updated_successfully[rules.language()]
    
    @classmethod
    def error_unknown_attribute(cls):
        return cls._error_unknown_attribute[rules.language()]

    @classmethod
    def bonuses_updated_successfully(cls):
        return cls._bonuses_updated_successfully[rules.language()]
        







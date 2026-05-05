
# Python module imports
import logging

from typing import Any

# internal imports
#   main package
from pen_n_paperless.common.keys import Specializations as keys
from pen_n_paperless.common.keys import Generic, Statistics, Traits, Abilities, Attributes, Professions

from pen_n_paperless.common.languages import Language
from pen_n_paperless.config.general import GeneralConfig

#   this submodule
from  ..character_properties_itf import CharacterPropertiesInterface
from .profession import Profession



class Specialization(CharacterPropertiesInterface):

    _specializations = {
        keys.PICKPOCKET: {
            Generic.DESCRIPTION: [""],

            keys.EVOLUTION: [
                {
                    Statistics.LEVEL: 2,
                    Generic.NAME: {
                        Language.ENGLISH: "Pickpocket", 
                        Language.GERMAN: "Taschendieb"
                        },
                    Traits.TRAIT: [
                        Traits.IMPERSONATOR,
                        Traits.LOCKSMITH,
                        Traits.TRAP_DIFFUSER
                        ]
                },
                {
                    Statistics.LEVEL: 4,
                    Generic.NAME: {
                        Language.ENGLISH: "Bandit", 
                        Language.GERMAN: "Straßenräuber"
                        },
                    Traits.TRAIT: [
                        Traits.STREET_SMARTS,
                        Traits.SMUGGLER,
                        Traits.FENCE_CONTACTS
                        ]
                },
                {
                    Statistics.LEVEL: 6,
                    Generic.NAME: {
                        Language.ENGLISH: "The Godfather", 
                        Language.GERMAN: "Der Pate"
                        },
                }
            ]
        },
        keys.ASSASSIN: {
            Generic.DESCRIPTION: [""],

            keys.EVOLUTION: [
                {
                    Statistics.LEVEL: 2,
                    Generic.NAME: {
                        Language.ENGLISH: "Assassin", 
                        Language.GERMAN: "Assassine"
                        },
                    Traits.TRAIT: [
                        Traits.NIGHTVISION,
                        Traits.MINDCONTROL,
                        Traits.HIDDEN_BLADE
                        ]
                },
                {
                    Statistics.LEVEL: 4,
                    Generic.NAME: {
                        Language.ENGLISH: "The Phantom", 
                        Language.GERMAN: "Das Phantom"
                        },
                    Abilities.ACROBATICS: 2,
                    Abilities.SNEAKING: 2,
                    Attributes.DEXTERITY_BONUS: 1
                },
                {
                    Statistics.LEVEL: 6,
                    Generic.NAME: {
                        Language.ENGLISH: "Shadow King", 
                        Language.GERMAN: "Schattenkönig"
                        },
                    Abilities.ACROBATICS: 1,
                    Attributes.DEXTERITY_BONUS: 1,
                    Attributes.INTELLIGENCE_BONUS: 1,
                    Abilities.SNEAKING: 2
                }
            ]
        }
    }




    @classmethod
    def get_all(cls) -> list:
        """
        Returns a list of all available specializations
        
        :param cls: Description
        :return: List of all available specializations as keys, empty list if no specializations exist
        :rtype: list
        """
        
        return list(cls._specializations.keys())


    @classmethod
    def get_properties(cls, key) -> dict:
        """
        Returns the properties of a specialization.
        
        :param cls: Description
        :param key: A specialization key. Can be obtained by calling get_all()
        :return: Properties of the specialization, empty dict if key does not exist.
        :rtype: dict[Any, Any]
        """

        return cls._specializations.get(key, {})
        

    @classmethod
    def get_all_names(cls) -> dict:
        specialization_dict = {}

        for s_key in cls.get_all():
            properties = cls.get_properties(s_key)
            evolutions = properties.get(keys.EVOLUTION, [])

            if evolutions == []:
                logging.warning(f"get_all_names(): get_all() returned the key {s_key}, but get_properties() did not include a value for key {keys.EVOLUTION}")
                specialization_dict[Generic.NONE] = "No specialization found"
            else:
                # add entry to dict with specialization key and its display name
                specialization_dict[s_key] = [evo.get(Generic.NAME, {}).get(GeneralConfig.language(), "") for evo in evolutions]

        return specialization_dict
    

    @classmethod
    def get_available(cls, profession_key: Professions, character_level: int) -> dict:

        specialization_dict = {}

        # check if a profession has already been selected
        if not profession_key:
            specialization_dict["None"] = "Select a profession first"
        else:
            for s_key in Profession.get_properties(profession_key).get(keys.SPECIALIZATION, []):
                specialization_dict[s_key] = cls.get_name(s_key, character_level)

        return specialization_dict


    @classmethod
    def get_name(cls, specialization_key, character_level) -> str:
        """Helper method

        Returns the highest ranking name from the given specialization
        
        :param cls: Description
        :param specialization_key: Description
        :param character_level: Description
        :return: Description
        :rtype: str
        """

        name = "Specialization not yet unlocked."

        # get the name of the highest unlocked evolution
        evolution_list = cls.get_properties(specialization_key).get(keys.EVOLUTION, [])

        if evolution_list:
            for evolution in evolution_list:
                if character_level >= evolution.get(Statistics.LEVEL):
                    name = evolution.get(Generic.NAME)[GeneralConfig.language()]
        else:
            logging.warning(f"Could not retrieve a list of the evolution steps for the specialization with the key {specialization_key}.")
            name = ""

        return name


    @classmethod
    def get_attribute_bonus(cls, specialization_key: keys, character_level: int, attribute_bonus_key: Attributes, default_value: int = 0) -> int:
        bonus = default_value

        evolution_list: list = cls.get_properties(specialization_key).get(keys.EVOLUTION, [])
        if evolution_list:
            for evolution in evolution_list:
                if character_level >= evolution.get(Statistics.LEVEL):
                    bonus += evolution.get(attribute_bonus_key, 0)

        return bonus


    # @classmethod
    # def attribute_bonus(cls, specialization_name: str, attribute_bonus_name, character_level) -> int:
    #     """returns the attribute bonus from the given specialization"""
    #     bonus = 0

    #     # iterate through list of evolutions
    #     spec_dict = cls._specializations.get(specialization_name, {})
    #     evo_array = spec_dict.get(Strings.Specialization.evolution.value, [])

    #     for num in evo_array:
    #         if character_level > num.get(Strings.Specialization.required_level.value):
    #             # attribute bonus accumulates when leveling up
    #             bonus +=  num.get(attribute_bonus_name, 0)
        
    #     return bonus
    

    # @classmethod
    # def ability_bonus(cls, specialization_name, ability_name, character_level) -> int:
    #     """returns the ability bonus from the given specialization"""
    #     bonus = 0

    #     for evolution in cls._specializations.get(specialization_name, "").get(Strings.Specialization.evolution.value, []):
    #         if character_level > evolution.get(Strings.Specialization.required_level.value):
    #             # attribute bonus accumulates when leveling up
    #             bonus += evolution.get(ability_name)
        
    #     return bonus






    


    
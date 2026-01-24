

# Python module imports
import logging

# internal imports
#   main package
from pen_n_paperless.common.keys import Tribes as key
from pen_n_paperless.common.keys import Generic, Attributes, Armour

from pen_n_paperless.common.languages import Language
from pen_n_paperless.config.general import GeneralConfig

#   this submodule
from ..character_properties_itf import CharacterPropertiesInterface



class Tribe(CharacterPropertiesInterface):

    # Tribe properties
    _tribes = {
        key.ELF: {
            Generic.NAME: {
                Language.ENGLISH: "Elves",
                Language.GERMAN: "Elfen"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A wandering tribe known for their adaptability and survival skills.", 
                Language.GERMAN: "",
            },
            Attributes.CHARISMA_BONUS: 1,
            Attributes.DEXTERITY_BONUS: 1,
            Attributes.STRENGTH_BONUS: -1,
        },
        key.GNOME: {
            Generic.NAME: {
                Language.ENGLISH: "Gnomes",
                Language.GERMAN: "Gnome"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A fierce warrior tribe known for their strength and combat prowess."
                },
            Attributes.DEXTERITY_BONUS: 1,
            Attributes.INTELLIGENCE_BONUS: 1,
            Attributes.STRENGTH_BONUS: -2,
            Armour.DEFENSE_BONUS: 1,
        },
        key.HALFELF: {
            Generic.NAME: {
                Language.ENGLISH: "Half-Elves",
                Language.GERMAN: "Halbelfen"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A tribe of skilled artisans and traders, known for their intelligence and charisma."
                },
            Attributes.CHARISMA_BONUS: 2,
            Attributes.ENDURANCE_BONUS: -1,
            Attributes.STRENGTH_BONUS: -1,
        },
        key.HALFLING: {
            Generic.NAME: {
                Language.ENGLISH: "Halflings",
                Language.GERMAN: "Halblinge"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A small and nimble tribe known for their stealth and agility."
                },
            Attributes.CHARISMA_BONUS: 1,
            Attributes.DEXTERITY_BONUS: 1,
            Attributes.STRENGTH_BONUS: -1,
            Armour.DEFENSE_BONUS: 1,
        },
        key.HALFORC: {
            Generic.NAME: {
                Language.ENGLISH: "Half-Orcs",
                Language.GERMAN: "Halborcs"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A tough and resilient tribe known for their endurance and fortitude."
                },
            Attributes.STRENGTH_BONUS: 2,
            Attributes.ENDURANCE_BONUS: 2,
            Attributes.CHARISMA_BONUS: -1,
            Attributes.INTELLIGENCE_BONUS: -1,
        },
        key.HUMAN: {
            Generic.NAME: {
                Language.ENGLISH: "Humans",
                Language.GERMAN: "Menschen"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A versatile and ambitious tribe known for their adaptability and resourcefulness."
                },
            Attributes.INTELLIGENCE_BONUS: 1,
        },
        key.DWARF: {
            Generic.NAME: {
                Language.ENGLISH: "Dwarfs",
                Language.GERMAN: "Zwerge"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A sturdy and hardworking tribe known for their craftsmanship and loyalty."
                },
            Attributes.ENDURANCE_BONUS: 1,
            Attributes.STRENGTH_BONUS: 1,
            Attributes.CHARISMA_BONUS: -1,
            Armour.DEFENSE_BONUS: 1,
        }
    }



    @classmethod
    def get_all(cls) -> list:
        """
        Return a list of all available tribe keys.
        
        :param cls: Description
        :return: Description
        :rtype: list[Any]
        """

        return list(cls._tribes.keys())


    @classmethod
    def get_properties(cls, key) -> dict:
        """
        Return the property dict for a given tribe name.

        :param cls: Description
        :param key: Description
        :return: Empty dict when the tribe is unknown.
        :rtype: dict[Any, Any]
        """

        return cls._tribes.get(key, {})


    @classmethod
    def get_all_names(cls) -> dict:
        """
        Returns a dict containing all tribe keys and their corresponding names.
        
        :param cls: Description
        :return: Description
        :rtype: dict[Any, Any]
        """
        tribe_dict = {}

        for t_key in cls.get_all():
            properties = cls.get_properties(t_key)
            name_dict = properties.get(Generic.NAME, {})

            if name_dict == {}:
                logging.warning(f"get_all_names(): get_all() returned the key {t_key}, but get_properties() did not include a value for key {Generic.NAME}")
                tribe_dict[Generic.NONE] = "No tribe found"
            else:
                # add entry to dict with tribe key and its display name
                tribe_dict[t_key] = name_dict.get(GeneralConfig.language(), "")

        return tribe_dict





    # @classmethod
    # def get_name(cls, tribe_key: str) -> str:
    #     """returns the language-dependent name of the tribe"""

    #     tribe_name = cls.get_properties(tribe_key).get(Strings.names.value)
    #     if not tribe_name:
    #         return "Error"
        
    #     return tribe_name[GameSettings.language()]



# Python module imports
import logging


# internal imports
#   main package
from pen_n_paperless.common.keys import Armour as key
from pen_n_paperless.common.keys import Generic

from pen_n_paperless.common.languages import Language
from pen_n_paperless.config.general import GeneralConfig


#   this submodule
from ..character_properties_itf import CharacterPropertiesInterface



class Armoury(CharacterPropertiesInterface):
    """Simple armour registry with a public API.

    Use Armoury.get_all() to get available armour names and
    Armoury.get_properties(name) to inspect an armour's properties.
    """

    # central registry of armour types and their properties
    # static attribute
    _armour = {
        key.WOOL: {
            Generic.NAME: {
                Language.ENGLISH: "Wool armour",
                Language.GERMAN: "Stoffrüstung"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "",
            },
            key.DEFENSE_BONUS: 1,
            Generic.WEIGHT: 5,
        },
        key.LEATHER: {
            Generic.NAME: {
                Language.ENGLISH: "Leather armour", 
                Language.GERMAN: "Lederrüstung"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "Lightweight armour offering minimal protection.",
            },
            key.DEFENSE_BONUS: 2,
            Generic.WEIGHT: 8,
        },
        key.CHAINMAIL: {
            Generic.NAME: {
                Language.ENGLISH: "Chainmail armour", 
                Language.GERMAN: "Kettenrüstung"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "Medium armour providing balanced protection and mobility.",
                Language.GERMAN: ""
            },
            key.DEFENSE_BONUS: 3,
            Generic.WEIGHT: 30,
        },
        key.COMPOSITE: {
            Generic.NAME: {
                Language.ENGLISH: "Composite armour", 
                Language.GERMAN: "Komposit-Rüstung"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "",
            },
            key.DEFENSE_BONUS:5,
            Generic.WEIGHT: 20,
        },
        key.PLATE: {
            Generic.NAME: {
                Language.ENGLISH: "Plate armour", 
                Language.GERMAN: "Plattenrüstung"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "Heavy armour offering maximum protection at the cost of mobility.",
            },
            key.DEFENSE_BONUS: 6,
            Generic.WEIGHT: 70,
        }
    }



    @classmethod
    def get_all(cls) -> list:
        """
        Return a list of all available sets of armour
        
        :param cls: Description
        :return: Description
        :rtype: list[Any]
        """
        return list(cls._armour.keys())


    @classmethod
    def get_properties(cls, key) -> dict:
        """
        Return the property dict for a given armour name.     
        
        :param cls: Description
        :param key: Description
        :type key: str
        :return: Empty dict when the armour is unknown. 
        :rtype: dict[Any, Any]
        """
        return cls._armour.get(key, {})


    @classmethod
    def get_all_names(cls) -> dict:

        armour_dict = {}

        for a_key in Armoury.get_all():
            properties = Armoury.get_properties(a_key)
            name_dict = properties.get(Generic.NAME, {})

            if name_dict == {}:
                logging.warning(f"get_all_names(): get_all() returned the key {a_key}, but get_properties() did not include a value for key {Generic.NAME}")
                armour_dict[Generic.NONE] = "No armour found"
            else:
                armour_dict[a_key] = name_dict.get(GeneralConfig.language(), "")

        return armour_dict
    



    @classmethod
    def get_name(cls, armour_key) -> str:
        """Get the name of a certain armour
        
        """
        return cls.get_properties(armour_key).get(Generic.NAME, {}).get(GeneralConfig.language(), "")

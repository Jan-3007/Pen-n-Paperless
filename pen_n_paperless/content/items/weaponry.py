

# Python module imports
import logging


# internal imports
#   main package
from pen_n_paperless.common.keys import Weapons as key
from pen_n_paperless.common.keys import Generic, Armour

from pen_n_paperless.common.languages import Language
from pen_n_paperless.config.general import GeneralConfig


#   this submodule
from ..character_properties_itf import CharacterPropertiesInterface


class Weaponry(CharacterPropertiesInterface):

    # weapon properties
    _weapons = {
        key.LONGSWORD: {
            Generic.NAME: {
                Language.ENGLISH: "Longsword", 
                Language.GERMAN: "Langschwert"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 0,
            key.ATTACK_BONUS: 3,
            Generic.WEIGHT: 0,
        },
        key.DAGGER: {
            Generic.NAME: {
                Language.ENGLISH: "Dagger", 
                Language.GERMAN: "Dolch"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 2,
            key.ATTACK_BONUS: 1,
            Generic.WEIGHT: 0,
        },
        key.TWO_HANDED_SWORD: {
            Generic.NAME: {
                Language.ENGLISH: "Two-handed sword", 
                Language.GERMAN: "Bihänder"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: -1,
            key.ATTACK_BONUS: 5,
            Generic.WEIGHT: 0,
        },
        key.FALCATA: {
            Generic.NAME: {
                Language.ENGLISH: "Falcata", 
                Language.GERMAN: "Falcata"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 1,
            key.ATTACK_BONUS: 3,
            Generic.WEIGHT: 0,
        },
        key.EPEE: {
            Generic.NAME: {
                Language.ENGLISH: "Epee", 
                Language.GERMAN: "Degen"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 3,
            key.ATTACK_BONUS: 2,
            Generic.WEIGHT: 0,
        },
        key.CUTLAS: {
            Generic.NAME: {
                Language.ENGLISH: "Cutlas", 
                Language.GERMAN: "Hirschfänger"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 2,
            key.ATTACK_BONUS: 1,
            Generic.WEIGHT: 0,
        },
        key.DAMASCENE_BLADE: {
            Generic.NAME: {
                Language.ENGLISH: "Damascene blade", 
                Language.GERMAN: "Damaszenerklinge"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 1,
            key.ATTACK_BONUS: 4,
            Generic.WEIGHT: 0,
        },
        key.CLAYMORE: {
            Generic.NAME: {
                Language.ENGLISH: "Claymore", 
                Language.GERMAN: "Flamberg"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 0,
            key.ATTACK_BONUS: 6,
            Generic.WEIGHT: 0,
        },
        key.HATCHET: {
            Generic.NAME: {
                Language.ENGLISH: "Hatchet", 
                Language.GERMAN: "Kriegsbeil"
            },
            Generic.DESCRIPTION: "",
            key.INI_BONUS: 1,
            key.ATTACK_BONUS: 2,
            Generic.WEIGHT: 0,
        },
        key.BATTLEAXE: {
            Generic.NAME: {
                Language.ENGLISH: "Battleaxe", 
                Language.GERMAN: "Streitaxt"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 0,
            key.ATTACK_BONUS: 3,
            Generic.WEIGHT: 0,
        },
        key.THROWING_AXE: {
            Generic.NAME: {
                Language.ENGLISH: "Throwing axe", 
                Language.GERMAN: "Wurfaxt"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 1,
            key.ATTACK_BONUS: 2,
            Generic.WEIGHT: 0,
        },
        key.JAVELIN: {
            Generic.NAME: {
                Language.ENGLISH: "Javelin", 
                Language.GERMAN: "Wurfspieß"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 2,
            key.ATTACK_BONUS: 2,
            Generic.WEIGHT: 0,
        },
        key.LANCE: {
            Generic.NAME: {
                Language.ENGLISH: "Lance", 
                Language.GERMAN: "Lanze"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 2,
            key.ATTACK_BONUS: 0,
            Generic.WEIGHT: 0,
        },
        key.PIKE: {
            Generic.NAME: {
                Language.ENGLISH: "Pike", 
                Language.GERMAN: "Langspeer"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 0,
            key.ATTACK_BONUS: 2,
            Generic.WEIGHT: 0,
        },
        key.HALBERD: {
            Generic.NAME: {
                Language.ENGLISH: "Halberd", 
                Language.GERMAN: "Hellebarde"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 0,
            key.ATTACK_BONUS: 3,
            Generic.WEIGHT: 0,
        },
        key.STAFF: {
            Generic.NAME: {
                Language.ENGLISH: "Staff", 
                Language.GERMAN: "Stab"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 2,
            key.ATTACK_BONUS: 0,
            Generic.WEIGHT: 0,
        },
        key.SHORTBOW: {
            Generic.NAME: {
                Language.ENGLISH: "Shortbow", 
                Language.GERMAN: "Kurzbogen"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 2,
            key.ATTACK_BONUS: 1,
            Generic.WEIGHT: 0,
        },
        key.LONGBOW: {
            Generic.NAME: {
                Language.ENGLISH: "Longbow", 
                Language.GERMAN: "Langbogen"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: -1,
            key.ATTACK_BONUS: 3,
            Generic.WEIGHT: 0,
        },
        key.COMPOSITE_BOW: {
            Generic.NAME: {
                Language.ENGLISH: "Composite bow", 
                Language.GERMAN: "Kompositbogen"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            key.INI_BONUS: 2,
            key.ATTACK_BONUS: 4,
            Generic.WEIGHT: 0,
        },
        key.ROUND_SHIELD: {
            Generic.NAME: {
                Language.ENGLISH: "Round shield", 
                Language.GERMAN: "LangschRundschildwert"
            },
            Generic.DESCRIPTION: {
                Language.ENGLISH: ""
            },
            Armour.DEFENSE_BONUS: 3,
            Generic.WEIGHT: 0,
        },
    }



    @classmethod
    def get_all(cls) -> list:
        """
        Return a list of all available weapons.
        
        :param cls: Description
        :return: Description
        :rtype: list[str]
        """
        return list(cls._weapons.keys())


    @classmethod
    def get_properties(cls, key) -> dict:
        """
        Return the property dict for a given armour name.     

        :param cls: Description
        :param key: Description
        :return: Description
        :rtype: dict[Any, Any]
        """
        return cls._weapons.get(key, {})


    @classmethod
    def get_all_names(cls) -> dict:
        """
        Get a dict with all available weapons.
        
        :param cls: Description
        :return: A dict containing weapon keys as keys and the corresponding name as value.
        :rtype: dict[Any, Any]
        """
        weapons_dict = {}

        for w_key in Weaponry.get_all():
            properties = Weaponry.get_properties(w_key)
            name_dict = properties.get(Generic.NAME, {})

            if name_dict == {}:
                logging.warning(f"get_all_names(): get_all() returned the key {w_key}, but get_properties() did not include a value for key {Generic.NAME}")
                weapons_dict[Generic.NONE] = "No weapon found"
            else:
                weapons_dict[w_key] = name_dict.get(GeneralConfig.language(), "")

        return weapons_dict
    


    # @classmethod
    # def get_name(cls, weapon_key: str) -> str:
    #     """Get the name of a certain weapon in the selected language"""
    #     name = cls.get_properties(weapon_key).get(Generic.NAME, "Empty")
    #     if isinstance(name, list):
    #         return name[GameSettings.language()]
    #     else:
    #         return name

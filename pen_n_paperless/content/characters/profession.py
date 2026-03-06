


# Python module imports
import logging

# internal imports
#   main package
from pen_n_paperless.common.keys import Professions as key
from pen_n_paperless.common.keys import Generic, Statistics, Specializations

from pen_n_paperless.common.languages import Language
from pen_n_paperless.config.general import GeneralConfig

#   this submodule
from  ..character_properties_itf import CharacterPropertiesInterface



class Profession(CharacterPropertiesInterface):


    # profession properties
    _professions = {
        key.BARD: {
            Generic.NAME: {
                Language.ENGLISH: "Bard",
                Language.GERMAN: "Barde"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A charismatic performer and storyteller, skilled in music and persuasion."
                },
            Specializations.SPECIALIZATION: [
                Specializations.SPY, 
                Specializations.ARTIST
                ],
            Statistics.HP: 4,
        },
        key.THIEF: {
            Generic.NAME: {
                Language.ENGLISH: "Thief",
                Language.GERMAN: "Dieb"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A cunning and stealthy individual, adept at sneaking and lockpicking."
                },
            Specializations.SPECIALIZATION: [
                Specializations.PICKPOCKET, 
                Specializations.ASSASSIN
                ],
            Statistics.HP: 6,
        },
        key.HERBALIST: {
            Generic.NAME: {
                Language.ENGLISH: "Herbalist", 
                Language.GERMAN: "Kräuterkundiger"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A knowledgeable healer and potion maker, skilled in the use of herbs and natural remedies."
                },
            Specializations.SPECIALIZATION: [
                Specializations.CHEMIST, 
                Specializations.HEALER
                ],
            Statistics.HP: 6,
        },
        key.WARRIOR: {
            Generic.NAME: {
                Language.ENGLISH: "Warrior", 
                Language.GERMAN: "Krieger"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A strong and skilled fighter, trained in the art of combat."
                },
            Specializations.SPECIALIZATION: [
                Specializations.BERSERKER, 
                Specializations.BOXER, 
                Specializations.SOLDIER, 
                Specializations.GUARD
                ],
            Statistics.HP: 10,
        },
        key.RANGER: {
            Generic.NAME: {
                Language.ENGLISH: "Ranger", 
                Language.GERMAN: "Waldläufer"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "A skilled tracker and hunter, adept at surviving in the wilderness."
                },
            Specializations.SPECIALIZATION: [
                Specializations.SCOUT, 
                Specializations.BEASTMASTER
                ],
            Statistics.HP: 8,
        },
        key.SCIENTIST: {
            Generic.NAME: {
                Language.ENGLISH: "Scientist", 
                Language.GERMAN: "Wissenschaftler"
                },
            Generic.DESCRIPTION: {
                Language.ENGLISH: "An intellectual and curious individual, skilled in the pursuit of knowledge and discovery."
                },
            Specializations.SPECIALIZATION: [
                Specializations.ALCHEMIST, 
                Specializations.GEOLOGIST, 
                Specializations.MATHEMATICIAN, 
                Specializations.PHARMACIST
                ],
            Statistics.HP: 3,
        },
    }


    
    @classmethod
    def get_all(cls) -> list:
        """
        Returns a list of all available professions
        
        :param cls: Description
        :return: List of all available professions as keys, empty list if no professions exist
        :rtype: list
        """

        return list(cls._professions.keys())


    @classmethod
    def get_properties(cls, key) -> dict:
        """
        Returns the properties of a profession.
        
        :param cls: Description
        :param key: A profession key. Can be obtained by calling get_all()
        :return: Properties of the profession, empty dict if key does not exist.
        :rtype: dict[Any, Any]
        """
        
        return cls._professions.get(key, {})


    @classmethod
    def get_all_names(cls) -> dict:
        profession_dict = {}

        for p_key in cls.get_all():
            properties = cls.get_properties(p_key)
            name_dict = properties.get(Generic.NAME, {})

            if name_dict == {}:
                logging.warning(f"get_all_names(): get_all() returned the key {p_key}, but get_properties() did not include a value for key {Generic.NAME}")
                profession_dict[Generic.NONE] = "No profession found"
            else:
                # add entry to dict with profession key and its display name
                profession_dict[p_key] = name_dict.get(GeneralConfig.language(), "")

        return profession_dict


    @classmethod
    def get_name(cls, profession_key) -> str:
        """returns the language-dependent name of the tribe"""

        profession_name = cls.get_properties(profession_key).get(Generic.NAME)
        if not profession_name:
            logging.warning(f"Tribe with key '{profession_key}' has no entry for key {Generic.NAME}")
            return "Error"
        
        return profession_name.get(GeneralConfig.language(), "Error")
    

    
    # @classmethod
    # def get_specializations(cls, profession_key) -> dict:
    #     """Returns all specializations available for a specific profession"""
    #     return cls._professions.get(profession_key, {}).get(Strings.specialization.value, [])

    # @classmethod
    # def name(self, profession_name) -> str:
    #     """returns the language-dependent name of the profession"""
    #     return self._professions[profession_name][Strings.names.value][rules.language]


    


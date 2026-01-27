from ..game_settings import GameSettings 
from ..strings import Strings

from .profession import Profession


class Specialization():

    _specializations = {
        Strings.Specialization.pickpocket.value: {
            Strings.description.value: [""],

            Strings.Specialization.evolution.value: [
                {
                    Strings.Specialization.required_level.value: 2,
                    Strings.names.value: ["Pickpocket", "Taschendieb"],
                    Strings.Abilities.abilities.value: [
                                        Strings.Abilities.impersonator.value,
                                        Strings.Abilities.locksmith.value,
                                        Strings.Abilities.trap_difuser.value]
                },
                {
                    Strings.Specialization.required_level.value: 4,
                    Strings.names.value: ["Bandit", "Straßenräuber"],
                    Strings.Abilities.abilities.value: [Strings.Abilities.street_smarts.value,
                                        Strings.Abilities.smuggler.value,
                                        Strings.Abilities.fence_contacts.value]
                },
                {
                    Strings.Specialization.required_level.value: 6,
                    Strings.names.value: ["The Godfather", "Der Pate"],
                }
            ]
        },
        Strings.Specialization.assassin.value: {
            Strings.description.value: [""],

            Strings.Specialization.evolution.value: [
                {
                    Strings.Specialization.required_level.value: 2,
                    Strings.names.value: ["Assassin", "Assassine"],
                    Strings.Abilities.abilities.value: [Strings.Abilities.nightvision.value,
                                        Strings.Abilities.mindcontrol.value,
                                        Strings.Abilities.hidden_blade.value]
                },
                {
                    Strings.Specialization.required_level.value: 4,
                    Strings.names.value: ["The Phantom", "Das Phantom"],
                    Strings.Abilities.acrobatics.value: 2,
                    Strings.Attributes.dexterity_bonus.value: 1,
                    Strings.Abilities.sneaking.value: 2
                },
                {
                    Strings.Specialization.required_level.value: 6,
                    Strings.names.value: ["Shadow King", "Schattenkönig"],
                    Strings.Abilities.acrobatics.value: 1,
                    Strings.Attributes.dexterity_bonus.value: 1,
                    Strings.Attributes.intelligence_bonus.value: 1,
                    Strings.Abilities.sneaking.value: 2
                }
            ]
        }
    }






    @classmethod
    def get_properties(cls, specialization_name) -> dict:
        """returns tribe properties"""
        return cls._specializations.get(specialization_name, {})
        

    @classmethod
    def attribute_bonus(cls, specialization_name: str, attribute_bonus_name, character_level) -> int:
        """returns the attribute bonus from the given specialization"""
        bonus = 0

        # iterate through list of evolutions
        spec_dict = cls._specializations.get(specialization_name, {})
        evo_array = spec_dict.get(Strings.Specialization.evolution.value, [])

        for num in evo_array:
            if character_level > num.get(Strings.Specialization.required_level.value):
                # attribute bonus accumulates when leveling up
                bonus +=  num.get(attribute_bonus_name, 0)
        
        return bonus
    

    @classmethod
    def ability_bonus(cls, specialization_name, ability_name, character_level) -> int:
        """returns the ability bonus from the given specialization"""
        bonus = 0

        for evolution in cls._specializations.get(specialization_name, "").get(Strings.Specialization.evolution.value, []):
            if character_level > evolution.get(Strings.Specialization.required_level.value):
                # attribute bonus accumulates when leveling up
                bonus += evolution.get(ability_name)
        
        return bonus


    @classmethod
    def get_name(self, specialization_key, character_level) -> str:
        """returns the current name from the given specialization"""

        name = "No specialization unlocked yet"

        # get the name of the highest unlocked evolution
        evolution_list = self._specializations.get(specialization_key, {}).get(Strings.Specialization.evolution.value, [])

        if evolution_list:
            for evolution in evolution_list:
                if character_level > evolution.get(Strings.Specialization.required_level.value):
                    name = evolution.get(Strings.names.value)[GameSettings.language()]

        return name


    @classmethod
    def get_all(cls) -> list[str]:
        """returns a list of all available specializations"""
        
        return list(cls._specializations.keys())


    @classmethod
    def get_all_names(cls, profession_key: str, character_level: int) -> dict:

        specialization_list = {}

        # check if a profession has already been selected
        if not profession_key:
            specialization_list["None"] = "Select a profession first"
        else:
            for s in Profession.get_specializations(profession_key):
                specialization_list[s] = Specialization.get_name(s, character_level)

        return specialization_list
    


    
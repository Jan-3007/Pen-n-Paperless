from ..game_settings import GameSettings
from ..strings import Strings



class Profession():


    # profession properties
    _professions = {
        Strings.Professions.bard.value: {
            Strings.names.value: ["Bard", "Barde"],
            Strings.description.value: ["A charismatic performer and storyteller, skilled in music and persuasion."],
            Strings.specialization.value: [Strings.Specialization.spy.value, 
                                        Strings.Specialization.artist.value],
            Strings.Statistics.max_hp.value: 4,
        },
        Strings.Professions.thief.value: {
            Strings.names.value: ["Thief", "Dieb"],
            Strings.description.value: "A cunning and stealthy individual, adept at sneaking and lockpicking.",
            Strings.specialization.value: [Strings.Specialization.pickpocket.value, 
                                            Strings.Specialization.assassin.value],
            Strings.Statistics.max_hp.value: 6,
        },
        Strings.Professions.herbalist.value: {
            Strings.names.value: ["Herbalist", "Kräuterkundiger"],
            Strings.description.value: "A knowledgeable healer and potion maker, skilled in the use of herbs and natural remedies.",
            Strings.specialization.value: [Strings.Specialization.chemist.value, 
                                                    Strings.Specialization.healer.value],
            Strings.Statistics.max_hp.value: 6,
        },
        Strings.Professions.warrior.value: {
            Strings.names.value: ["Warrior", "Krieger"],
            Strings.description.value: "A strong and skilled fighter, trained in the art of combat.",
            Strings.specialization.value: [Strings.Specialization.berserker.value, 
                                                    Strings.Specialization.boxer.value, 
                                                    Strings.Specialization.soldier.value, 
                                                    Strings.Specialization.guard.value],
            Strings.Statistics.max_hp.value: 10,
        },
        Strings.Professions.ranger.value: {
            Strings.names.value: ["Ranger", "Waldläufer"],
            Strings.description.value: "A skilled tracker and hunter, adept at surviving in the wilderness.",
            Strings.specialization.value: [Strings.Specialization.scout.value, 
                                                    Strings.Specialization.beastmaster.value],
            Strings.Statistics.max_hp.value: 8,
        },
        Strings.Professions.scientist.value: {
            Strings.names.value: ["Scientist", "Wissenschaftler"],
            Strings.description.value: "An intellectual and curious individual, skilled in the pursuit of knowledge and discovery.",
            Strings.specialization.value: [Strings.Specialization.alchemist.value, 
                                                    Strings.Specialization.geologist.value, 
                                                    Strings.Specialization.mathematician.value, 
                                                    Strings.Specialization.pharmacist.value],
            Strings.Statistics.max_hp.value: 3,
        },
    }


    @classmethod
    def get_properties(cls, profession_key) -> dict:
        """Returns profession properties"""
        return cls._professions.get(profession_key, {})

    @classmethod
    def get_specializations(cls, profession_key) -> dict:
        """Returns all specializations available for a specific profession"""
        return cls._professions.get(profession_key, {}).get(Strings.specialization.value, [])

    # @classmethod
    # def name(self, profession_name) -> str:
    #     """returns the language-dependent name of the profession"""
    #     return self._professions[profession_name][Strings.names.value][rules.language]


    @classmethod
    def get_all(cls) -> list[str]:
        """Returns a list of all available professions"""

        return list(cls._professions.keys())
    

    @classmethod
    def get_all_names(cls) -> dict:
        profession_list = {}

        for p in Profession.get_all():
            profession_dict = Profession.get_properties(p)
            profession_name = profession_dict.get(Strings.names.value, [])

            if not profession_name:
                profession_list["None"] = "No professions found"
            else:
                # add entry to dict with profession key and its display name
                profession_list[p] = profession_name[GameSettings.language()]

        return profession_list

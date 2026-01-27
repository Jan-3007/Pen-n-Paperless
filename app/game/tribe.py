from ..game_settings import GameSettings
from ..strings import Strings




class Tribe():
    """Simple tribe registry with public API"""

    # Tribe properties
    _tribes = {
        Strings.Tribes.elf.value: {
            Strings.names.value: ["Elves", "Elfen"],
            Strings.description.value: ["A wandering tribe known for their adaptability and survival skills.", 
                                    ""],
            Strings.Attributes.charisma_bonus.value: 1,
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Attributes.strength_bonus.value: -1,
        },
        Strings.Tribes.gnome.value: {
            Strings.names.value: ["Gnomes", "Gnome"],
            Strings.description.value: ["A fierce warrior tribe known for their strength and combat prowess."],
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Attributes.intelligence_bonus.value: 1,
            Strings.Attributes.strength_bonus.value: -2,
            Strings.Armour.defense_bonus.value: 1,
        },
        Strings.Tribes.halfelf.value: {
            Strings.names.value: ["Half-Elves", "Halbelfen"],
            Strings.description.value: ["A tribe of skilled artisans and traders, known for their intelligence and charisma."],
            Strings.Attributes.charisma_bonus.value: 2,
            Strings.Attributes.endurance_bonus.value: -1,
            Strings.Attributes.strength_bonus.value: -1,
        },
        Strings.Tribes.halfling.value: {
            Strings.names.value: ["Halflings", "Halblinge"],
            Strings.description.value: ["A small and nimble tribe known for their stealth and agility."],
            Strings.Attributes.charisma_bonus.value: 1,
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Attributes.strength_bonus.value: -1,
            Strings.Armour.defense_bonus.value: 1,
        },
        Strings.Tribes.halforc.value: {
            Strings.names.value: ["Half-Orcs", "Halborcs"],
            Strings.description.value: ["A tough and resilient tribe known for their endurance and fortitude."],
            Strings.Attributes.strength_bonus.value: 2,
            Strings.Attributes.endurance_bonus.value: 2,
            Strings.Attributes.charisma_bonus.value: -1,
            Strings.Attributes.intelligence_bonus.value: -1,
        },
        Strings.Tribes.human.value: {
            Strings.names.value: ["Humans", "Menschen"],
            Strings.description.value: ["A versatile and ambitious tribe known for their adaptability and resourcefulness."],
            Strings.Attributes.intelligence_bonus.value: 1,
        },
        Strings.Tribes.dwarf.value: {
            Strings.names.value: ["Dwarfs", "Zwerge"],
            Strings.description.value: ["A sturdy and hardworking tribe known for their craftsmanship and loyalty."],
            Strings.Attributes.endurance_bonus.value: 1,
            Strings.Attributes.strength_bonus.value: 1,
            Strings.Attributes.charisma_bonus.value: -1,
            Strings.Armour.defense_bonus.value: 1,
        }
    }


    @classmethod
    def get_properties(cls, tribe_key: str) -> dict:
        """Return the property dict for a given tribe name.

        Returns an empty dict when the tribe is unknown.
        """
        return cls._tribes.get(tribe_key, {})


    @classmethod
    def get_name(cls, tribe_key: str) -> str:
        """returns the language-dependent name of the tribe"""

        tribe_name = cls.get_properties(tribe_key).get(Strings.names.value)
        if not tribe_name:
            return "Error"
        
        return tribe_name[GameSettings.language()]


    @classmethod
    def get_all(cls) -> list:
        """Return a list of all available tribe names."""
        return list(cls._tribes.keys())


    @classmethod
    def get_all_names(cls) -> dict:

        tribe_list = {}

        for t in Tribe.get_all():
            tribe_name = Tribe.get_name(t)

            if not tribe_name:
                tribe_list["None"] = "No tribe name found"
            else:
                # add entry to dict with tribe key and its display name
                tribe_list[t] = tribe_name

        return tribe_list



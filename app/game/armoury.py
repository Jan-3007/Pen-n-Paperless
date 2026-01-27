from ..strings import Strings
from ..game_settings import GameSettings

class Armoury:
    """Simple armour registry with a public API.

    Use Armoury.get_all() to get available armour names and
    Armoury.get_properties(name) to inspect an armour's properties.
    """

    # central registry of armour types and their properties
    # static attribute
    _armour = {
        Strings.Armour.wool.value: {
            Strings.names.value: ["Wool armour", "Stoffrüstung"],
            Strings.description.value: "",
            Strings.Armour.defense_bonus.value: 1,
            Strings.weight.value: 5,
        },
        Strings.Armour.leather.value: {
            Strings.names.value: ["Leather armour", "Lederrüstung"],
            Strings.description.value: "Lightweight armour offering minimal protection.",
            Strings.Armour.defense_bonus.value: 2,
            Strings.weight.value: 8,
        },
        Strings.Armour.chainmail.value: {
            Strings.names.value: ["Chainmail armour", "Kettenrüstung"],
            Strings.description.value: "Medium armour providing balanced protection and mobility.",
            Strings.Armour.defense_bonus.value: 3,
            Strings.weight.value: 30,
        },
        Strings.Armour.composite.value: {
            Strings.names.value: ["Composite armour", "Komposit-Rüstung"],
            Strings.description.value: "",
            Strings.Armour.defense_bonus.value:5,
            Strings.weight.value: 20,
        },
        Strings.Armour.plate.value: {
            Strings.names.value: ["Plate armour", "Plattenrüstung"],
            Strings.description.value: "Heavy armour offering maximum protection at the cost of mobility.",
            Strings.Armour.defense_bonus.value: 6,
            Strings.weight.value: 70,
        }
    }



    @classmethod
    def get_properties(cls, armour_key: str) -> dict:
        """Return the property dict for a given armour name.

        Returns an empty dict when the armour is unknown.
        """
        return cls._armour.get(armour_key, {})

    @classmethod
    def get_all(cls) -> list:
        """Return a list of all available armour keys."""
        return list(cls._armour.keys())


    @classmethod
    def get_name(cls, armour_key: str) -> str:
        """Get the name of a certain armour in the selected language"""
        name = cls.get_properties(armour_key).get(Strings.names.value, "Empty")
        if isinstance(name, list):
            return name[GameSettings.language()]
        else:
            return name
    


    @classmethod
    def get_all_names(cls) -> dict:

        armour_list = {}

        for a in Armoury.get_all():
            armour_dict = Armoury.get_properties(a)
            armour_name = armour_dict.get(Strings.names.value, [])

            if not armour_name:
                armour_list["None"] = "No armour name found"
            else:
                armour_list[a] = armour_name[GameSettings.language()]

        return armour_list
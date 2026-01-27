from ..strings import Strings
from ..game_settings import GameSettings


class Weaponry():

    # weapon properties
    _weapons = {
        Strings.Weapons.longsword.value: {
            Strings.names.value: ["Longsword", "Langschwert"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 0,
            Strings.Weapons.attack_bonus.value: 3,
            Strings.weight.value: 0,
        },
        Strings.Weapons.dagger.value: {
            Strings.names.value: ["Dagger", "Dolch"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 2,
            Strings.Weapons.attack_bonus.value: 1,
            Strings.weight.value: 0,
        },
        Strings.Weapons.two_handed_sword.value: {
            Strings.names.value: ["Two-handed sword", "Bihänder"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: -1,
            Strings.Weapons.attack_bonus.value: 5,
            Strings.weight.value: 0,
        },
        Strings.Weapons.falcata.value: {
            Strings.names.value: ["Falcata", "Falcata"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 1,
            Strings.Weapons.attack_bonus.value: 3,
            Strings.weight.value: 0,
        },
        Strings.Weapons.epee.value: {
            Strings.names.value: ["Epee", "Degen"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 3,
            Strings.Weapons.attack_bonus.value: 2,
            Strings.weight.value: 0,
        },
        Strings.Weapons.cutlas.value: {
            Strings.names.value: ["Cutlas", "Hirschfänger"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 2,
            Strings.Weapons.attack_bonus.value: 1,
            Strings.weight.value: 0,
        },
        Strings.Weapons.damascene_blade.value: {
            Strings.names.value: ["Damascene blade", "Damaszenerklinge"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 1,
            Strings.Weapons.attack_bonus.value: 4,
            Strings.weight.value: 0,
        },
        Strings.Weapons.claymore.value: {
            Strings.names.value: ["Claymore", "Flamberg"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 0,
            Strings.Weapons.attack_bonus.value: 6,
            Strings.weight.value: 0,
        },
        Strings.Weapons.hatchet.value: {
            Strings.names.value: ["Hatchet", "Kriegsbeil"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 1,
            Strings.Weapons.attack_bonus.value: 2,
            Strings.weight.value: 0,
        },
        Strings.Weapons.battleaxe.value: {
            Strings.names.value: ["Battleaxe", "Streitaxt"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 0,
            Strings.Weapons.attack_bonus.value: 3,
            Strings.weight.value: 0,
        },
        Strings.Weapons.throwing_axe.value: {
            Strings.names.value: ["Throwing axe", "Wurfaxt"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 1,
            Strings.Weapons.attack_bonus.value: 2,
            Strings.weight.value: 0,
        },
        Strings.Weapons.javelin.value: {
            Strings.names.value: ["Javelin", "Wurfspieß"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 2,
            Strings.Weapons.attack_bonus.value: 2,
            Strings.weight.value: 0,
        },
        Strings.Weapons.lance.value: {
            Strings.names.value: ["Lance", "Lanze"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 2,
            Strings.Weapons.attack_bonus.value: 0,
            Strings.weight.value: 0,
        },
        Strings.Weapons.pike.value: {
            Strings.names.value: ["Pike", "Langspeer"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 0,
            Strings.Weapons.attack_bonus.value: 2,
            Strings.weight.value: 0,
        },
        Strings.Weapons.halberd.value: {
            Strings.names.value: ["Halberd", "Hellebarde"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 0,
            Strings.Weapons.attack_bonus.value: 3,
            Strings.weight.value: 0,
        },
        Strings.Weapons.staff.value: {
            Strings.names.value: ["Staff", "Stab"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 2,
            Strings.Weapons.attack_bonus.value: 0,
            Strings.weight.value: 0,
        },
        Strings.Weapons.shortbow.value: {
            Strings.names.value: ["Shortbow", "Kurzbogen"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 2,
            Strings.Weapons.attack_bonus.value: 1,
            Strings.weight.value: 0,
        },
        Strings.Weapons.longbow.value: {
            Strings.names.value: ["Longbow", "Langbogen"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: -1,
            Strings.Weapons.attack_bonus.value: 3,
            Strings.weight.value: 0,
        },
        Strings.Weapons.composite_bow.value: {
            Strings.names.value: ["Composite bow", "Kompositbogen"],
            Strings.description.value: "",
            Strings.Weapons.ini_bonus.value: 2,
            Strings.Weapons.attack_bonus.value: 4,
            Strings.weight.value: 0,
        },
        Strings.Weapons.round_shield.value: {
            Strings.names.value: ["Round shield", "Rundschild"],
            Strings.description.value: "",
            Strings.Armour.defense_bonus: 3,
            Strings.weight.value: 0,
        },
    }



    @classmethod
    def get_properties(cls, weapon_name) -> dict:
        """returns weapon properties"""
        return cls._weapons.get(weapon_name, {})


    @classmethod
    def get_all(cls) -> list[str]:
        """returns a list of all available weapons"""
        return list(cls._weapons.keys())
    

    @classmethod
    def get_name(cls, weapon_key: str) -> str:
        """Get the name of a certain weapon in the selected language"""
        name = cls.get_properties(weapon_key).get(Strings.names.value, "Empty")
        if isinstance(name, list):
            return name[GameSettings.language()]
        else:
            return name


    @classmethod
    def get_all_names(cls) -> dict:

        weapon_list = {}

        for w in Weaponry.get_all():
            weapon_dict = Weaponry.get_properties(w)
            weapon_name = weapon_dict.get(Strings.names.value, [])

            if not weapon_name:
                weapon_list["None"] = "No weapon name found"
            else:
                weapon_list[w] = weapon_name[GameSettings.language()]

        return weapon_list
    

    
from ..strings import Strings
from ..game_settings import GameSettings

class Abilities:
    """Simple ability registry with a public API.

    Use Abilities.get_all() to get available ability names and
    Abilities.get_properties(name) to inspect an abilities properties.
    """

    # central registry of armour types and their properties
    # static attribute
    _abilities = {
        Strings.Abilities.acrobatics.value: {
            Strings.names.value: ["Acrobatics", "Akrobatik"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                Strings.Professions.bard.value: [1],
                Strings.Professions.thief.value: [1,2],
                Strings.Professions.herbalist.value: [6],
                Strings.Professions.warrior.value: [4],
                Strings.Professions.ranger.value: [2],
                Strings.Professions.scientist.value: [6],
            }
        },
        Strings.Abilities.athletics.value: {
            Strings.names.value: ["Athletics", "Athletik"],
            Strings.description.value: "",
            Strings.Attributes.endurance_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value: [2],
                Strings.Professions.thief.value: [2],
                Strings.Professions.herbalist.value: [4],
                Strings.Professions.warrior.value: [1],
                Strings.Professions.ranger.value: [2],
                Strings.Professions.scientist.value: [6],
            }
        },
        Strings.Abilities.intimidation.value: {
            Strings.names.value: ["Intimidation", "Einschüchterung"],
            Strings.description.value: "",
            Strings.Attributes.charisma_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value: [3],
                Strings.Professions.thief.value: [4],
                Strings.Professions.herbalist.value: [6],
                Strings.Professions.warrior.value: [1],
                Strings.Professions.ranger.value: [2],
                Strings.Professions.scientist.value: [6],
            }
        },
        Strings.Abilities.poison_mixing.value: {
            Strings.names.value: ["Poison mixing", "Giftmischen"],
            Strings.description.value: "",
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [4],
                Strings.Professions.thief.value:        [6],
                Strings.Professions.herbalist.value:    [1],
                Strings.Professions.warrior.value:      [],
                Strings.Professions.ranger.value:       [],
                Strings.Professions.scientist.value:    [1],
            }
        },
        Strings.Abilities.healing.value: {
            Strings.names.value: ["Healing", "Heilen"],
            Strings.description.value: "",
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [5,6],
                Strings.Professions.thief.value:        [],
                Strings.Professions.herbalist.value:    [1,3],
                Strings.Professions.warrior.value:      [],
                Strings.Professions.ranger.value:       [],
                Strings.Professions.scientist.value:    [1,2],
            }
        },
        Strings.Abilities.inspiration.value: {
            Strings.names.value: ["Inspiration", "Inspiration"],
            Strings.description.value: "",
            Strings.Attributes.charisma_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [2],
                Strings.Professions.thief.value:        [8],
                Strings.Professions.herbalist.value:    [8],
                Strings.Professions.warrior.value:      [1],
                Strings.Professions.ranger.value:       [4],
                Strings.Professions.scientist.value:    [8],
            }
        },
        Strings.Abilities.culture.value: {
            Strings.names.value: ["Culture", "Kultur"],
            Strings.description.value: "",
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [1,2],
                Strings.Professions.thief.value:        [4,6],
                Strings.Professions.herbalist.value:    [4,6],
                Strings.Professions.warrior.value:      [5,6],
                Strings.Professions.ranger.value:       [3,5],
                Strings.Professions.scientist.value:    [2,4],
            }
        },
        Strings.Abilities.art.value: {
            Strings.names.value: ["Art", "Kunst"],
            Strings.description.value: "",
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [1],
                Strings.Professions.thief.value:        [4],
                Strings.Professions.herbalist.value:    [5],
                Strings.Professions.warrior.value:      [6],
                Strings.Professions.ranger.value:       [4],
                Strings.Professions.scientist.value:    [3],
            }
        },
        Strings.Abilities.cunning.value: {
            Strings.names.value: ["Cunning", "List"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Attributes.intelligence_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3],
                Strings.Professions.thief.value:        [1],
                Strings.Professions.herbalist.value:    [6],
                Strings.Professions.warrior.value:      [3],
                Strings.Professions.ranger.value:       [3],
                Strings.Professions.scientist.value:    [6],
            }
        },
        Strings.Abilities.medicine.value: {
            Strings.names.value: ["Medicine", "Medizin"],
            Strings.description.value: "",
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3,5],
                Strings.Professions.thief.value:        [],
                Strings.Professions.herbalist.value:    [2,3],
                Strings.Professions.warrior.value:      [],
                Strings.Professions.ranger.value:       [4,5],
                Strings.Professions.scientist.value:    [1,2],
            }
        },
        Strings.Abilities.nature.value: {
            Strings.names.value: ["Nature", "Natur"],
            Strings.description.value: "",
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3],
                Strings.Professions.thief.value:        [6],
                Strings.Professions.herbalist.value:    [2],
                Strings.Professions.warrior.value:      [4],
                Strings.Professions.ranger.value:       [1],
                Strings.Professions.scientist.value:    [5],
            }
        },
        Strings.Abilities.riding.value: {
            Strings.names.value: ["Riding", "Reiten"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [2],
                Strings.Professions.thief.value:        [3],
                Strings.Professions.herbalist.value:    [4],
                Strings.Professions.warrior.value:      [1],
                Strings.Professions.ranger.value:       [1],
                Strings.Professions.scientist.value:    [6],
            }
        },
        Strings.Abilities.sneaking.value: {
            Strings.names.value: ["Sneaking", "Schleichen"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [1,3],
                Strings.Professions.thief.value:        [1,2],
                Strings.Professions.herbalist.value:    [2,4],
                Strings.Professions.warrior.value:      [4,5],
                Strings.Professions.ranger.value:       [1,3],
                Strings.Professions.scientist.value:    [5,6],
            }
        },
        Strings.Abilities.swimming.value: {
            Strings.names.value: ["Swimming", "Schwimmen"],
            Strings.description.value: "",
            Strings.Attributes.endurance_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3],
                Strings.Professions.thief.value:        [3],
                Strings.Professions.herbalist.value:    [4],
                Strings.Professions.warrior.value:      [2],
                Strings.Professions.ranger.value:       [1],
                Strings.Professions.scientist.value:    [4],
            }
        },
        Strings.Abilities.animal_care.value: {
            Strings.names.value: ["Animal care", "Tierumgänglichkeit"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [2],
                Strings.Professions.thief.value:        [5],
                Strings.Professions.herbalist.value:    [4],
                Strings.Professions.warrior.value:      [4],
                Strings.Professions.ranger.value:       [1],
                Strings.Professions.scientist.value:    [5],
            }
        },
        Strings.Abilities.survival.value: {
            Strings.names.value: ["Survival", "Überleben"],
            Strings.description.value: "",
            Strings.Abilities.max_upgrades_per_level.value: 1,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3],
                Strings.Professions.thief.value:        [5],
                Strings.Professions.herbalist.value:    [2],
                Strings.Professions.warrior.value:      [2],
                Strings.Professions.ranger.value:       [1],
                Strings.Professions.scientist.value:    [4],
            }
        },
        Strings.Abilities.conviction.value: {
            Strings.names.value: ["Conviction", "Überzeugung"],
            Strings.description.value: "",
            Strings.Attributes.charisma_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [1,3],
                Strings.Professions.thief.value:        [2,4],
                Strings.Professions.herbalist.value:    [3,5],
                Strings.Professions.warrior.value:      [4,5],
                Strings.Professions.ranger.value:       [3,4],
                Strings.Professions.scientist.value:    [2,4],
            }
        },
        Strings.Abilities.investigation.value: {
            Strings.names.value: ["Investigation", "Untersuchung"],
            Strings.description.value: "",
            Strings.Attributes.intelligence_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [1,3],
                Strings.Professions.thief.value:        [2,3],
                Strings.Professions.herbalist.value:    [3,5],
                Strings.Professions.warrior.value:      [2,4],
                Strings.Professions.ranger.value:       [2,3],
                Strings.Professions.scientist.value:    [4,5],
            }
        },
        Strings.Abilities.weapons1.value: {
            Strings.names.value: ["Weapons", "Waffen"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Attributes.strength_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3,4],
                Strings.Professions.thief.value:        [2,4],
                Strings.Professions.herbalist.value:    [3,5],
                Strings.Professions.warrior.value:      [1,3],
                Strings.Professions.ranger.value:       [2,4],
                Strings.Professions.scientist.value:    [4,6],
            }
        },
        Strings.Abilities.weapons2.value: {
            Strings.names.value: ["Weapons", "Waffen"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Attributes.strength_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3,4],
                Strings.Professions.thief.value:        [2,4],
                Strings.Professions.herbalist.value:    [3,5],
                Strings.Professions.warrior.value:      [1,3],
                Strings.Professions.ranger.value:       [2,4],
                Strings.Professions.scientist.value:    [4,6],
            }
        },
        Strings.Abilities.weapons3.value: {
            Strings.names.value: ["Weapons", "Waffen"],
            Strings.description.value: "",
            Strings.Attributes.dexterity_bonus.value: 1,
            Strings.Attributes.strength_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [3,4],
                Strings.Professions.thief.value:        [2,4],
                Strings.Professions.herbalist.value:    [3,5],
                Strings.Professions.warrior.value:      [1,3],
                Strings.Professions.ranger.value:       [2,4],
                Strings.Professions.scientist.value:    [4,6],
            }
        },
        Strings.Abilities.perception.value: {
            Strings.names.value: ["Perception", "Wahrnehmung"],
            Strings.description.value: "",
            Strings.Attributes.intelligence_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [1,3],
                Strings.Professions.thief.value:        [1,2],
                Strings.Professions.herbalist.value:    [2,4],
                Strings.Professions.warrior.value:      [2,4],
                Strings.Professions.ranger.value:       [2,3],
                Strings.Professions.scientist.value:    [3,5],
            }
        },
        Strings.Abilities.knowledge.value: {
            Strings.names.value: ["Knowledge", "Wissen"],
            Strings.description.value: "",
            Strings.Attributes.intelligence_bonus.value: 1,
            Strings.Abilities.max_upgrades_per_level.value: 2,
            Strings.Abilities.cost.value: {
                # [cost for +1 level, cost for +2 levels, ...]
                Strings.Professions.bard.value:         [1,2],
                Strings.Professions.thief.value:        [3,4],
                Strings.Professions.herbalist.value:    [2,4],
                Strings.Professions.warrior.value:      [4,5],
                Strings.Professions.ranger.value:       [3,5],
                Strings.Professions.scientist.value:    [2,3],
            }
        },
    }



    @classmethod
    def get_properties(cls, ability_key: str) -> dict:
        """Return the property dict for a given ability name.

        Returns an empty dict when the ability is unknown.
        """
        return cls._abilities.get(ability_key, {})
    
    @classmethod
    def get_all(cls) -> list:
        """Return a list of all available ability keys."""
        return list(cls._abilities.keys())
    
    @classmethod
    def get_cost(cls, ability_key: str, profession_key: str) -> list:
        """Return the cost list for a given ability and profession.

        Returns an empty list when the ability or profession is unknown.
        """
        ability_props = cls.get_properties(ability_key)
        cost_dict = ability_props.get(Strings.Abilities.cost.value, {})
        return cost_dict.get(profession_key, ["Select a profession to see costs"])
    



    @classmethod
    def get_all_names(cls, profession_key) -> dict:
        ability_list = {}

        for a in Abilities.get_all():
            ability_dict = Abilities.get_properties(a)
            ability_name = ability_dict.get(Strings.names.value, [])

            if not ability_name:
                ability_list["None"] = "No ability name found"
            else:
                ability_list[a] = {
                    Strings.names.value: ability_name[GameSettings.language()],
                    Strings.Abilities.max_upgrades_per_level.value: ability_dict.get(Strings.Abilities.max_upgrades_per_level.value, 0),
                    Strings.Abilities.cost.value: Abilities.get_cost(a, profession_key)
                }

        return ability_list

    '''
    ability key:
    {
        current level : ability level,
        cost history : [int],
    }
    '''
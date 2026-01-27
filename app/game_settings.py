from .languages import Language



"""Contains static non-changeable game rules"""
class GameSettings:


    # game world properties
    _world_name = "Aborea"
    _default_language = Language.GERMAN.value

    # character properties
    _total_attribute_points = 35
    _max_armour_sets = 1
    _max_nb_weapons = 2





    @classmethod
    def world_name(cls) -> str:
        """The name of the game world."""
        return cls._world_name
    
    @classmethod
    def language(cls) -> int:
        """The default language of the game."""
        return cls._default_language

    @classmethod
    def total_attribute_points(cls) -> int:
        """Total attribute points available to a character."""
        return cls._total_attribute_points

    @classmethod
    def max_armour_sets(cls) -> int:
        """Max. amount of armour sets allowed per player"""
        return int(cls._max_armour_sets)
    
    @classmethod
    def max_number_of_weapons(cls) -> int:
        """Max. number of weapons allowed per player"""
        return int(cls._max_nb_weapons)


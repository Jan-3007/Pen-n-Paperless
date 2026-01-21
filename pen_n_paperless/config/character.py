


class CharacterConfig():
    _total_attribute_points = 35
    _max_armour_sets = 1
    _max_nb_weapons = 2
    
    
    @classmethod
    def total_attribute_points(cls) -> int:
        return cls._total_attribute_points
    
    @classmethod
    def max_armour_sets(cls) -> int:
        return cls._max_armour_sets
    
    @classmethod
    def max_number_of_weapons(cls) -> int:
        return cls._max_nb_weapons
    



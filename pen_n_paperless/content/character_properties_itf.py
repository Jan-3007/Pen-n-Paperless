
# Python module imports
from abc import ABC, abstractmethod


# internal imports




class CharacterPropertiesInterface(ABC):

    @classmethod
    @abstractmethod
    def get_all(cls) -> list:
        """
        Returns a list of all keys
        
        :param cls: Description
        :return: Description
        :rtype: list[str]
        """
        pass
    
    @classmethod
    @abstractmethod
    def get_properties(cls, key) -> dict:
        """
        Returns the data associated with the key
        
        :param cls: Description
        :param key: Description
        :return: Description
        :rtype: dict[Any, Any]
        """
        pass
    
    @classmethod
    @abstractmethod
    def get_all_names(cls) -> dict:
        """
        Returns a dict with key-name pairs
        
        :param cls: Description
        :return: Description
        :rtype: dict[Any, Any]
        """
        pass






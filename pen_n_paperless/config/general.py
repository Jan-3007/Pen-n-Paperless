# Python module imports
import logging

# internal module imports
from ..common.languages import Language


class GeneralConfig():
    _world_name = "Pen'n'Paperless"
    _language = Language.ENGLISH

    # log level one of: DEBUG, INFORMATION, WARNING, ERROR, CRITICAL
    _log_level = logging.DEBUG

    # max. avatar size: (width, height)
    _avatar_size = (512, 1024)


    @classmethod
    def world_name(cls) -> str:
        """The name of the game world."""
        return cls._world_name
    
    @classmethod
    def language(cls) -> Language:
        """The default language of the Web UI"""
        return cls._language
    
    @classmethod
    def log_level(cls) -> logging._Level | None:
        """The log level of the python application"""
        return cls._log_level
    
    @classmethod
    def avatar_size(cls) -> tuple:
        """Returns the max width and max height respectively of the avatar
        """
        return cls._avatar_size
    

# Python module imports
from enum import auto

# internal module imports
from pen_n_paperless.common.keys import Key


class StatusCode(Key):
    """Enum containing all status codes

    """

    def __repr__(self) -> str:
        return str(self.value)

    STATUS = auto()
    ERROR = auto()
    WARNING = auto()
    SUCCESS = auto()



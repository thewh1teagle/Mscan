import platform
from enum import Enum
from functools import lru_cache

class Platform(Enum):
    LINUX = 'linux'
    MAC = 'darwin'
    WINDOWS = 'windows'

    @lru_cache()
    def __bool__(self):
        return platform.system().lower() == self.value

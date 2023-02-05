import platform
from enum import Enum


class Platform(Enum):
    LINUX = 'linux'
    MAC = 'darwin'
    WINDOWS = 'windows'

    def __bool__(self):
        return platform.system().lower() == self.value

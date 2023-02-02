import platform
from os import environ
from enum import Enum

class Platform(Enum):
    LINUX = 'linux'
    MAC = 'darwin'
    WINDOWS = 'windows'
    ANDROID = 'android'

    def __bool__(self):
        return (
            platform.system().lower() == self.value 
            or
            self.value == self.ANDROID and 'ANDROID_ARGUMENT' in environ
        )
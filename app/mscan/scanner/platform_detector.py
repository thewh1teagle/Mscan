import platform
from enum import Enum
from functools import lru_cache
from os import environ

class Platform(Enum):
    LINUX = 'linux'
    MAC = 'darwin'
    WINDOWS = 'windows'
    ANDROID = 'android'

    @lru_cache()
    def __bool__(self):
        # android
        if self.value == self.ANDROID: 
            return 'ANDROID_STORAGE' in environ
        # mac, windows, linux
        return platform.system().lower() == self.value

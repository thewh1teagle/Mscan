import platform
from os import environ
from enum import Enum

class Platform(Enum):
    LINUX = 'linux'
    MAC = 'darwin'
    WINDOWS = 'windows'
    ANDROID = 'android'

    _current_platform = None

    def __bool__(self):
        if self._current_platform is None:
            if platform.system().lower() == self.value or self.value == self.ANDROID and 'ANDROID_ARGUMENT' in environ:
                self._current_platform = True
            else:
                self._current_platform = False
        return self._current_platform

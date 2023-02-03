import subprocess
from .platform_detector import Platform

class Ping:
    """Cross platform ping"""
    def ping(self, ip, count = 1):
        count_flag = "-n" if Platform.WINDOWS else "-c"
        proc = subprocess.call(["ping", count_flag, str(count), ip], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return proc == 0


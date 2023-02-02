from queue import Queue
from typing import List
from icmplib import multiping
from .interface import InterfaceManager
from .network import Network
import asyncio


class MultiPinger:
    """ Multithreaded class for pinging hosts and display progress """
    def ping(self, ips: List[str]):
        res = multiping(ips, count=2, privileged=False)
        return res




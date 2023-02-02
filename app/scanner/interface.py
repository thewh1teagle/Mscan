import socket
import psutil
from pprint import pprint
from dataclasses import dataclass, asdict
import ipaddress
from typing import Any, List


@dataclass
class Interface:
    name: str
    address: str
    netmask: str
    family: int
    prefix_length: int

    @classmethod
    def from_psutil(cls, family, interface, snic):

        family = 6 if family == socket.AF_INET6 else 4
        netmask = snic.netmask
        if netmask:
            prefix_length = sum([bin(int(x)).count("1") for x in netmask.split(".")])
        else:
            prefix_length = None
        
        return cls(interface, snic.address, netmask, family, prefix_length)

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
    
    @classmethod
    def from_dict(cls, iface_dict):
        return cls(**iface_dict)

class InterfaceManager:

    def get_interfaces(self, family = socket.AF_INET):
        ifaces = psutil.net_if_addrs().items()
        for interface, snics in ifaces:
            for snic in snics:
                if snic.family == family:
                    yield Interface.from_psutil(family, interface, snic)

    def get_default(self, family = socket.AF_INET):
        ifaces = self.get_interfaces()
        sock_ifaces = socket.getaddrinfo(socket.gethostname(), None)
        sock_ifaces = list(filter(lambda s: s[0] == family, sock_ifaces))
        if sock_ifaces:
            first = sock_ifaces[0]
            addr = first[-1][0]
            return next((i for i in ifaces if i.address == addr), None)







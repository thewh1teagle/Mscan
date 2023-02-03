from dataclasses import dataclass
from typing import List
from .interface import Interface
import ipaddress

@dataclass
class Network:
    default_gateway: str
    ips: List[str]

    @classmethod
    def from_interface(cls, interface: Interface):
        network =  ipaddress.IPv4Network(f'{interface.address}/{interface.prefix_length}', strict=False)
        default_gateway = network[1]
        return cls(default_gateway, network)
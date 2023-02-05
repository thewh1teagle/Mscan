import ipaddress
from dataclasses import dataclass

from .interface import Interface


@dataclass
class Network:
    default_gateway: ipaddress.IPv4Address
    ips: ipaddress.IPv4Network

    @classmethod
    def from_interface(cls, interface: Interface):
        network = ipaddress.IPv4Network(f'{interface.address}/{interface.prefix_length}', strict=False)
        default_gateway = network[1]
        return cls(default_gateway, network)

from .interface import InterfaceManager, Interface
from .platform_detector import Platform
import subprocess
import re
from dataclasses import dataclass
from typing import List, Union

@dataclass
class Host:
    addr: str
    hwaddr: str
    addr_type: str

class Arp:
    
    @staticmethod
    def parse(output, iface_ip) -> List[Host]:
        lines = output.strip().split("\n")
        lines = [l.strip() for l in lines if l.strip() != ""]
        tables = {}
        current = None
        for line in lines:
            if line.startswith('Interface'):
                current = line.split()[1]
                tables[current] = []
            elif "Physical" not in line:
                addr, hwaddr, addr_type = line.split()
                row = Host(addr, hwaddr, addr_type)
                tables[current].append(row)
        return tables.get(iface_ip)

    @staticmethod
    def get_tables(interface: Interface):
        if Platform.WINDOWS:
            output = subprocess.run(["arp", "-a"], stdout=subprocess.PIPE).stdout.decode("utf-8")
            tables = Arp.parse(output, interface.address)
            return tables or []
        elif Platform.LINUX:
            hosts = []
            with open('/proc/net/arp', 'r') as f:
                lines = f.read().splitlines()
                lines = lines[1:]
            for line in lines:
                ip, hw_type, flags, hw_addr, _mask, ifname = line.split()
                print(ifname, interface.name)
                if ifname == interface.name and flags != "0x0":
                    hosts.append(Host(ip, hw_addr, hw_type))
            return hosts
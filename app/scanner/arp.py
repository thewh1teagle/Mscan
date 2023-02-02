from .interface import InterfaceManager
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


def get_tables(iface_ip):
    output = subprocess.run(["arp", "-a"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    tables = parse(output, iface_ip)
    return tables or []

from .interface import Interface
from .platform_detector import Platform
import subprocess
from dataclasses import dataclass
from typing import List
import ctypes
from ipaddress import IPv4Address
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
            proc = subprocess.run(["arp", "-a"], stdout=subprocess.PIPE)
            output = proc.stdout.decode("utf-8")
            tables = Arp.parse(output, interface.address)
            return tables or []
        elif Platform.LINUX:
            hosts = []
            with open('/proc/net/arp', 'r') as f:
                lines = f.read().splitlines()
                lines = lines[1:]
            for line in lines:
                ip, hw_type, flags, hw_addr, _mask, ifname = line.split()
                if ifname == interface.name and flags != "0x0":
                    hosts.append(Host(ip, hw_addr, hw_type))
            return hosts
        
    @staticmethod
    def get_mac(host):
        """ Send ARP who-has request using Microsoft's Iphlpapi.lib
        Args:
            host (str): IP address to request
        Returns:
            True if IP address answers to ARP who-has, False otherwise

        DWORD SendARP(
        _In_    IPAddr DestIP,
        _In_    IPAddr SrcIP,
        _Out_   PULONG pMacAddr,
        _Inout_ PULONG PhyAddrLen
        );

        DestIP is decimal value of inverted IP address, for instance :
        10.0.0.103 => 103.0.0.10 => 1728053258
        Microsoft recommands wsock32.inet_addr(), which I can't use with Python 3.
        """
        SendARP = ctypes.windll.Iphlpapi.SendARP
        #inetaddr = ctypes.windll.wsock32.inet_addr(host) #Fonctionne uniquement sous Python 2
        inetaddr = int(IPv4Address('.'.join(host.split(".")[::-1])))

        buffer = ctypes.c_buffer(6)
        addlen = ctypes.c_ulong(ctypes.sizeof(buffer))

        if SendARP(inetaddr, 0, ctypes.byref(buffer), ctypes.byref(addlen)) == 0:
            mac = buffer[:6]
            return mac.hex()
        return ''
from .interface import InterfaceManager, Interface
from .network import Network
from .multi_ping import MultiPinger
from scanner import arp
from dataclasses import dataclass, asdict
from mac_vendor_lookup import MacLookup
import dns.resolver
from typing import List

@dataclass
class LiveHost:
    ip: str
    mac: str
    vendor: str
    hostname: str

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}



BLACKLIST_PREFIX = [str(i) for i in range(220, 265)]
BLACKLIST_SUFFIX = ['255']

class Scanner:

    @staticmethod
    def get_vendor(mac: str):
        mac = mac.upper().replace('-', ':')
        vendor = "unknown"
        try:
            vendor = MacLookup().lookup(mac)
        except:
            pass
        return vendor

    @staticmethod
    def get_hostname(ip):
        """ Find local domain by ip """
        try:
            dns_raw_hostname = dns.reversename.from_address(ip)   
            dns_raw_hostname = dns_raw_hostname.to_text()
            myRes=dns.resolver.Resolver()
            myRes.timeout = 0.1
            myRes.lifetime = 0.1
            myRes.nameservers=['224.0.0.251'] #mdns multicast address
            myRes.port=5353 #mdns port
            hostname = myRes.resolve(dns_raw_hostname,'PTR')
            hostname = hostname[0].to_text()
            return hostname[:-1]
        except:
            pass
        return 'uknown'

    @staticmethod
    def scan(iface: Interface) -> List[LiveHost]:
        network = Network.from_interface(iface)
        ips = network.ips
        ips = [str(i) for i in ips]
        MultiPinger().ping(ips)
        hosts = arp.get_tables(iface.address)
        live_hosts = []
        for host in hosts:
            vendor = Scanner.get_vendor(host.hwaddr)
            hostname = Scanner.get_hostname(host.addr)
            live_host = LiveHost(host.addr, host.hwaddr, vendor, hostname)
            suffix = live_host.ip[-3:]
            prefix = live_host.ip[:3]
            if prefix not in BLACKLIST_PREFIX and suffix not in BLACKLIST_SUFFIX:
                live_hosts.append(live_host)
        return live_hosts
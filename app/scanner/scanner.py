from .interface import InterfaceManager, Interface
from .network import Network
from .multi_ping import MultiPinger
from scanner.arp import Arp, Host as ArpHost
from dataclasses import dataclass, asdict
from mac_vendor_lookup import MacLookup
import dns.resolver
from typing import List
import socket
import concurrent.futures

@dataclass
class LiveHost:
    ip: str
    mac: str
    vendor: str
    hostname: str

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


class Scanner:

    BLACKLIST_PREFIX = [str(i) for i in range(220, 265)]
    BLACKLIST_SUFFIX = ['255']


    def __init__(self) -> None:
        self.multi = MultiPinger()

    @property
    def progress(self):
        return self.multi.progress


    @staticmethod
    def get_hostnames(hosts: List[ArpHost], max_workers = 20):
        
        def job(host: ArpHost):
            try:
                hostname = socket.gethostbyaddr(host.addr)[0]
            except:
                hostname = "unknown"
            return {"host": host, "name": hostname}

        result = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executer:
            futures = []
            for host in hosts:
                futures.append(executer.submit(job, host))
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                host, name = res.values()
                result[host.addr] = name
        return result

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
    def get_live_hosts(hosts: List[ArpHost]):
        live_hosts = []
        ips = [i.addr for i in hosts]
        hostnames = Scanner.get_hostnames(hosts)
        for host in hosts:
            suffix = host.addr[-3:]
            prefix = host.addr[:3]
            if prefix not in Scanner.BLACKLIST_PREFIX and suffix not in Scanner.BLACKLIST_SUFFIX:
                vendor = Scanner.get_vendor(host.hwaddr)
                live_host = LiveHost(host.addr, host.hwaddr, vendor, hostnames.get(host.addr, "unknown"))
                live_hosts.append(live_host)
        return live_hosts

    def scan(self, iface: Interface) -> List[LiveHost]:
        network = Network.from_interface(iface)
        ips = [str(i) for i in network.ips] 
        self.multi.set_ips(ips)
        self.multi.start()
        self.multi.join()
        hosts = Arp.get_tables(iface.address)
        live = self.get_live_hosts(hosts)
        return live
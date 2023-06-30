import concurrent.futures
import socket
from dataclasses import dataclass, asdict
from typing import List
from mac_vendor_lookup import AsyncMacLookup
from .platform_detector import Platform
from .arp import Arp, Host as ArpHost
from .interface import Interface
from .multi_ping import MultiPinger
from .network import Network
import re

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

    @staticmethod
    def get_hostname(host):
        try:
            return socket.gethostbyaddr(host['ip'])[0]
        except:
            return ''

    @staticmethod
    def get_hostnames(hosts):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2500) as executer:
            results = []
            for host, result in zip(hosts, executer.map(Scanner.get_hostname, hosts)):
                if result:
                    results.append({**host, 'hostname': result})
        return results

    @staticmethod
    def get_hostnames(hosts: List[ArpHost], max_workers=2500):

        def job(arp_host: ArpHost):
            try:
                hostname = socket.gethostbyaddr(arp_host.addr)[0]
            except:
                hostname = "unknown"
            return {"host": arp_host, "name": hostname}

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
    async def get_vendor(mac: str):
        mac = mac.upper().replace('-', ':')
        try:
            vendor = await AsyncMacLookup().lookup(mac)
        except:
            return "unknown"
        return vendor

    @staticmethod
    async def get_live_hosts(hosts: List[ArpHost]):
        live_hosts = []
        hostnames = Scanner.get_hostnames(hosts)
        for host in hosts:
            suffix = host.addr[-3:]
            prefix = host.addr[:3]
            if prefix not in Scanner.BLACKLIST_PREFIX and suffix not in Scanner.BLACKLIST_SUFFIX:
                vendor = await Scanner.get_vendor(host.hwaddr)
                live_host = LiveHost(host.addr, host.hwaddr, vendor, hostnames.get(host.addr, "unknown"))
                live_hosts.append(live_host)
        return live_hosts


    def arp_scan(self, hosts):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2500) as executer:
            results = []
            for host, result in zip(hosts, executer.map(Arp.get_mac, hosts)):
                if result:
                    result = re.sub(r'(..)', r'\1:', result)[:-1]
                    result = result.upper()
                    results.append(ArpHost(addr=host, hwaddr=result, addr_type='dynamic'))
        return results
    
    async def scan(self, iface: Interface) -> List[LiveHost]:
        network = Network.from_interface(iface)
        ips = [str(i) for i in network.ips]
        if Platform.WINDOWS:
            hosts = self.arp_scan(ips)
        else:
            await MultiPinger().ping(ips)
            hosts = Arp.get_tables(iface)
        live = await self.get_live_hosts(hosts)
        return live

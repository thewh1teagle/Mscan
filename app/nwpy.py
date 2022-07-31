#!/usr/bin/env python3

import tableprint
import socket
import fcntl
import struct
import argparse
import os
import sys
import time
import dns.resolver
import subprocess
from queue import Queue
from threading import Thread
from netaddr import IPNetwork
from mac_vendor_lookup import MacLookup
from ipaddress import IPv4Address

def calc_percentage(part, whole):
    return str(int(( 100 * float(part)//float(whole) )))


def get_ip_address(ifname) -> str:
    """ Return the current ip address of the interface """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15].encode())
    )[20:24])


def get_default_iface_name_linux() -> str:
    """ Return the default network interface """
    route = "/proc/net/route"
    with open(route) as f:
        for line in f.readlines():
            try:
                iface, dest, _, flags, _, _, _, _, _, _, _, =  line.strip().split()
                if dest != '00000000' or not int(flags, 16) & 2:
                    continue
                return iface
            except:
                continue

def get_prefix(mask):
    """ calculate prefix by network mask """
    prefix = sum([bin(int(x)).count('1') for x in mask.split('.')])
    return prefix

def get_netmask(ifname):
    """ Find network mask by given interface """
    ifname = ifname.encode()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x891b, struct.pack(b'256s',ifname))[20:24]) 


def get_ips_of_network(ifname):
    """ Find possible ips in the current network """
    try:
        if not ifname:
            ifname = get_default_iface_name_linux()
        ip = get_ip_address(ifname)
        mask = get_netmask(ifname)
        network = IPNetwork('/'.join([ip, mask]))
        addresses = map(lambda ip: str(ip), network)
        return list(addresses)[1:-1]
    except OSError:
        print('Error. Interface {} was not found.'.format(ifname))
        sys.exit(1)


def get_arp_list(ifname):
    """ Find the current arp online clients """
    deafult_gateway = get_default_gateway_linux()
    PIPE, STDOUT = subprocess.PIPE, subprocess.STDOUT
    arpA_req = subprocess.Popen(
        ['arp', '-i', ifname, '-n'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    out, _err = arpA_req.communicate()
    out = out.decode().splitlines()
    addresses = []
    for address in out[1:]:
        address = address.split()
        
        if address[1] == "(incomplete)":
            continue
        
        
        if address[0] == deafult_gateway:
            addresses.insert(0,
                {'ip': address[0], 'mac': address[2]}
            )    
        else:
            addresses.append(
                {'ip': address[0], 'mac': address[2]}
            )
    return addresses




def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

def getHwAddr(ifname):
    """ Read mac address of interface """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])


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
        return 'Unknown'






class Pinger:
    """ Multithreaded class for pinging hosts and display progress """
    def __init__(self, ips: list):
        self.q = Queue()
        self.len_of_ips = len(ips)
        self.threads = []
        for ip in ips:
            self.q.put(ip)


    def start_workers(self, num = 30):
        self.threads.append(Thread(target=self.progress_worker))
        for _ in range(num):
            self.threads.append(Thread(target=self.scanner_worker))
        for worker in self.threads:
            worker.start()
        for worker in self.threads:
            worker.join()



    def progress_worker(self):
        while not self.q.empty():
            # print(self.q.qsize(), self.len_of_ips)
            percentage = calc_percentage(self.len_of_ips - self.q.qsize(), self.len_of_ips)
            sys.stdout.write(f"\rScanning... {percentage}%")

            time.sleep(0.01)
        print()
        print ("\033[A\033[A") # Clear last line

    def scanner_worker(self):
        while not self.q.empty():
            ip = self.q.get()
            self.ping(ip)

    def ping(self, ip):
        # print(f"pinging {ip}")
        for _ in range(2):
            response = os.system("timeout 0.1 ping -c 1 " + ip + " > /dev/null 2>&1")
            # and then check the response...
            if response == 0:
                return True
        return False

def list_interfaces():
    interfaces = socket.if_nameindex() 
    return [{'name': i[1]} for i in interfaces]


def fill_vendors(arp_data, default_gateway):
    l = len(arp_data)
    p = 0
    
    for section in arp_data:
        
        try: # Add mac vendors
            section['vendor'] = MacLookup().lookup(section['mac'])
        except:
            section['vendor'] = "Unknown"

        try: # Add local hostnames
            section['hostname'] = get_hostname(section['ip'])
        except:
            section['hostname'] = "Unknown"
        p += 1
        percentage = calc_percentage(p, l)
        sys.stdout.write(f"\rAnalyzing... {percentage}%")
    print()
    print ("\033[A\033[A") # Clear last line


def scan(ifname):
    ips = get_ips_of_network(ifname)
    pinger = Pinger(ips)
    pinger.start_workers()
    arp_data = get_arp_list(ifname) # [ (ip, mac) ]
    default_gateway = get_default_gateway_linux()
    fill_vendors(arp_data, default_gateway)
    
  
    # Insert my computer info into the scanned data
    my_mac = getHwAddr(ifname)
    arp_data.insert(1,
        {'ip': get_ip_address(ifname), 'mac': my_mac, 'vendor': MacLookup().lookup(my_mac), 'hostname': 'Your pc'}
    )
    arp_data.sort(key=lambda x: IPv4Address( x['ip'] ))
    return arp_data



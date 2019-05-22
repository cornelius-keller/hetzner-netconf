#!/usr/local/bin/python

from netifaces import interfaces, ifaddresses, gateways, AF_INET
from netaddr import IPNetwork, IPAddress
import subprocess
import re
from os import environ
from threading import Event

inetaddr = None
inetmask = None

for iface in interfaces():
    if (iface.startswith("en") or iface.startswith("eth")):
        ifconf = ifaddresses(iface)
        # AF_INET is not always present
        if AF_INET in ifconf.keys():
            for link in ifconf[AF_INET]:
                # loopback holds a 'peer' instead of a 'broadcast' address
                if 'addr' in link.keys() and 'peer' not in link.keys():
                    inetaddr = link['addr']
                    inetmask = link['netmask']
                    break
            # If we got the IPv4 addr & netmask, we can stop looping
            if inetaddr is not None and inetmask is not None:
                break


# get current route destinations
routes = subprocess.check_output("route")
destinations = []

for line in routes.split("\n"):
    if re.match("^\d+\.\d+\.\d+\.\d+.*", line):
        destinations.append(line.split()[0])

network = IPNetwork("%s/%s" % (inetaddr, inetmask))


gws = gateways()
default_gw = gws['default'][AF_INET]

for ip in network:
    if ip != network.network and ip != network.broadcast and ip != IPAddress(default_gw[0]) and str(ip) not in destinations:
        subprocess.call(["route", "add", "-host", str(ip),  "gw", default_gw[0]])

if environ.get('SET_ROUTES_NOWAIT') is None:
    Event().wait()

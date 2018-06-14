#!/usr/local/bin/python
import netifaces
import netaddr
import subprocess
import os
from threading import Event
import pprint 


for iface in netifaces.interfaces():
    if iface.startswith("en"):
        for ifconf in  netifaces.ifaddresses(iface)[netifaces.AF_INET]:
            if ifconf['netmask'] != '255.255.255.255':
               break


network = netaddr.IPNetwork("%s/%s" % (ifconf['addr'], ifconf['netmask']))


gws = netifaces.gateways()
default_gw = gws['default'][netifaces.AF_INET]

for ip in network:
    if ip != network.network and ip != network.broadcast and ip != netaddr.IPAddress(default_gw[0]):
        subprocess.call(["route", "add", "-host", str(ip),  "gw", default_gw[0]])

Event.wait()

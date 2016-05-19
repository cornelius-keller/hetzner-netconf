#!/usr/local/bin/python
import netifaces
import netaddr
import subprocess
import os

ifconf = netifaces.ifaddresses(os.environ.get("IFACE"))[netifaces.AF_INET][0]

network = netaddr.IPNetwork("%s/%s" % (ifconf['addr'], ifconf['netmask']))


gws = netifaces.gateways()
default_gw = gws['default'][netifaces.AF_INET]

for ip in network:
    if ip != network.network and ip != network.broadcast and ip != netaddr.IPAddress(default_gw[0]):
        subprocess.call(["route", "add", "-host", str(ip),  "gw", default_gw[0]])

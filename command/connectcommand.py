from lib.parser import SkyjackArgumentParser
from lib.pyiw import WirelessInterface
from termcolor import colored

info_str = colored("[*] ", "blue")
succ_str = colored("[+] ", "green")
erro_str = colored("[+] ", "red")

class ConnectCommand():

    def __init__(self, iface):
        self.cmd = "connect" 
        self.iface = WirelessInterface(iface)
        
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="")
        self.parser.add_argument("ssid", help="the ssid to connect to")

    def execute(self, args):
        "connect to a drone"

        self.iface.down()
        self.iface.set_mode("managed")
        self.iface.up()
        res = self.iface.connect(args.ssid)
        if res:
            print succ_str + "successfully connected to %s" % res
        else:
            print erro_str + "connection failed"
            return
        print info_str + "waiting for ip address..."
        self.iface.wait_for_ip()
        print info_str + "ip address acquired"

        



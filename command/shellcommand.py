from lib.parser import SkyjackArgumentParser
import telnetlib


class ShellCommand():

    def __init__(self):
        self.cmd = "shell" 
        
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="get a root shell on the connected drone")

    def execute(self, args):
        "get a root shell on the connected drone"

        try:
            tn = telnetlib.Telnet("192.168.1.1")
            tn.interact()
        except Exception as e:
            print "error: %s" % str(e)


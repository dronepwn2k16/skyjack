# wrapper functions for iw, some code adopted from
# https://github.com/Plippe/python-ip-iw
from subprocess import Popen, PIPE, call
import netifaces as ni
from time import sleep
import platform, os

class WirelessInterface():

    def __init__(self, iface):
        self.name = iface

    def connect(self, ssid):
        shell_cmd = ['iw', 'dev', self.name, 'connect', '-w', ssid]
	process = Popen(shell_cmd, stdout=PIPE, stderr=PIPE)
	stdout = process.communicate()[0].strip()
        if "connected to" in stdout:
            return stdout.split('connected to')[1].strip()
        else:
            return False

    def up(self):
	shell_cmd = "ifconfig {} up".format(self.name)
        return self._generic_execute(shell_cmd)

    def down(self):
	shell_cmd = "ifconfig {} down".format(self.name)
        return self._generic_execute(shell_cmd)

    def _generic_execute(self, shell_cmd):
	process = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
	process.wait()

	return True if process.returncode == 0 else False

    def get_mode(self):
	shell_cmd = "iw dev {} info | grep -i \"type\" | grep -ioe \"[a-z]*$\"".format(self.name)
	process = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
	stdout = process.communicate()[0].strip()

	return stdout

    def set_mode(self, value):
	possible_modes = ["monitor", "managed", "station", "wds", "mesh", "mp", "ibss", "adhoc"]

	if value not in possible_modes:
	    raise ValueError("\"{}\" is not a valid wireless mode.".format(value))

	shell_cmd = "iw dev {} set type {}".format(self.name, value)
        return self._generic_execute(shell_cmd)

    def set_channel(self, value):
	if not 1 <= value <= 14:
	    raise ValueError("\"{}\" is not a valid channel.".format(value))

	return self.__set("channel " + str(value))

    def __set(self, value):
	shell_cmd = "iw dev {} set {}".format(self.name, value)
	process = Popen(shell_cmd, shell=True, stdout=PIPE, stderr=PIPE)
	process.wait()

	return True if process.returncode == 0 else False

    def wait_for_ip(self):
        ip = None
        while not ip:
            try:
                if "arm" in platform.machine().lower():
                    ip = ni.ifaddresses(self.name)[ni.AF_INET]
                else:
                    os.system("dhclient %s &>/dev/null" % self.name)
                    ip = True
            except KeyError:
                pass
            sleep(0.1)
        return ip

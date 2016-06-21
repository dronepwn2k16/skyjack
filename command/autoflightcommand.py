from lib.parser import SkyjackArgumentParser
from telnetlib import Telnet
from lib.libardrone import ARDrone
from time import sleep
import sys

from termcolor import colored

info_str = colored("\t[*] ", "blue")
err_str = colored("\t[-] ", "red")
succ_str = colored("\t[+] ", "green")

class Autofligthcommand():

    def __init__(self):
        # this is the name by which the command will be invoked
        self.cmd = "auto"
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="hard coded flight routine")
        			 
 
    def execute(self, args):
        # the string below this line will be shown when the 'help' command is executed
        # it should be a short description of what it does
        'hard coded flight routine'
        # self.reset()
        # sleep(2)
        # command logic goes here:
        
        #self.testing()
        self.demo()


    def demo(self):
        drone = ARDrone()
        self.start(drone)
        drone.speed = 0.3
        self.up(drone, 1)
        self.forward(drone, 1)

        # clean exit
        drone.land()
        sleep(5)
        drone.halt()
        self.reset()


    def testing(self):
        drone = ARDrone()
        self.start(drone)

        self.forward(drone, 3)
        self.up(drone, 5)
        self.down(drone, 5)
        self.backward(drone, 3)

        # clean exit
        drone.land()
        sleep(5)
        drone.halt()
        self.reset()
        
    def start(self, drone):
        print info_str + "starting"
        drone.takeoff()
        sleep(5)
        drone.hover()
        sleep(1)
        print info_str + "start routine done"  
        return 0
        
        
    def forward(self, drone, i):
        print info_str + "forward %d " % i 
        drone.move_forward()
        sleep(i)
        drone.hover()
        sleep(1)
        print info_str + "forward routine done"
        return 0
 
    def backward(self, drone, i):
        print info_str + "backward %d " % i 
        drone.move_backward()
        sleep(i)
        drone.hover()
        sleep(1)
        print info_str + "backward routine done"
        return 0

    def up(self, drone, i):
        print info_str + "up %d " % i 
        drone.speed = 0.4
        drone.move_up()
        sleep(i)
        drone.hover()
        sleep(1)
        drone.speed = 0.1
        print info_str + "up routine done"
        return 0
       
    def down(self, drone, i):
        print info_str + "down %d " % i 
        drone.speed = 0.4
        drone.move_down()
        sleep(i)
        drone.hover()
        sleep(1)
        drone.speed = 0.1
        print info_str + "down routine done"
        return 0

    def turn(self, drone):
        print info_str + "turn " 
        drone.speed = 1
        for x in range(4):       
            drone.turn_left()
            sleep(0.20)
        drone.hover()
        sleep(1)
        drone.speed = 0.1
        print info_str + "turn routine done"
        return 0

    def reset(self):
        tn = Telnet('192.168.1.1')
        try:
            print succ_str + '[+] resetting drone'
            tn.read_until('#')

            # make
            self.tcmd('killall -9 program.elf', tn)
            tn.close()

        except Exception as e:
            print err_string + '[ERROR] telnet command execution failed'
            print e.message

        finally:
            tn.close()

    def tcmd(self, cmd, tn):
        print info_str + '[+] executing %s ' % cmd
        tn.write(cmd + '\n')
        print tn.read_until('#')

        return 0


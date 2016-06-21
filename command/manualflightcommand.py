from lib.parser import SkyjackArgumentParser
from telnetlib import Telnet
import pygame
from lib.libardrone import ARDrone
from termcolor import colored

info_str = colored("\t[*] ", "blue")
err_str = colored("\t[-] ", "red")
succ_str = colored("\t[+] ", "green")

class ManualFlightcommand():

    def __init__(self):
        # this is the name by which the command will be invoked
        self.cmd = "manual" 
        # this ArgumentParser will automatically be invoked when your command is executed
        # see https://docs.python.org/3/library/argparse.html for documentation
        # please make sure to always include the help parameter
        # you do not have to add -h/--help, this gets gernated automatically
        # make sure to set prog to self.cmd, otherwise it will print the ARGV[0] as command name
        self.parser = SkyjackArgumentParser(prog=self.cmd, description="manual drone flight")
        

    def invoke(self):
        return self.execute(None)


    # the execute method will be called when the command is invoked
    # args contains the results of your ArgumentParser.
    # the method will ONLY be executed if argument parsing was 
    # successful, so you do not have to care about that
    def execute(self, args):
        # the string below this line will be shown when the 'help' command is executed
        # it should be a short description of what it does
        'manual drone flight'

        # command logic goes here:

        pygame.init()
        W, H = 320, 220
        screen = pygame.display.set_mode((W, H))
        drone = ARDrone()
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
                elif event.type == pygame.KEYUP:
                    drone.hover()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        drone.reset()
                        running = False
                    # takeoff / land
                    elif event.key == pygame.K_RETURN:
                        drone.takeoff()
                    elif event.key == pygame.K_SPACE:
                        drone.land()
                    # emergency
                    elif event.key == pygame.K_BACKSPACE:
                        drone.reset()
                    # forward / backward
                    elif event.key == pygame.K_w:
                        drone.move_forward()
                    elif event.key == pygame.K_s:
                        drone.move_backward()
                    # left / right
                    elif event.key == pygame.K_a:
                        drone.move_left()
                    elif event.key == pygame.K_d:
                        drone.move_right()
                    # up / down
                    elif event.key == pygame.K_UP:
                        drone.move_up()
                    elif event.key == pygame.K_DOWN:
                        drone.move_down()
                    # turn left / turn right
                    elif event.key == pygame.K_LEFT:
                        drone.turn_left()
                    elif event.key == pygame.K_RIGHT:
                        drone.turn_right()
                    # speed
                    elif event.key == pygame.K_1:
                        drone.speed = 0.1
                    elif event.key == pygame.K_2:
                        drone.speed = 0.2
                    elif event.key == pygame.K_3:
                        drone.speed = 0.3
                    elif event.key == pygame.K_4:
                        drone.speed = 0.4
                    elif event.key == pygame.K_5:
                        drone.speed = 0.5
                    elif event.key == pygame.K_6:
                        drone.speed = 0.6
                    elif event.key == pygame.K_7:
                        drone.speed = 0.7
                    elif event.key == pygame.K_8:
                        drone.speed = 0.8
                    elif event.key == pygame.K_9:
                        drone.speed = 0.9
                    elif event.key == pygame.K_0:
                        drone.speed = 1.0

            try:
                surface = pygame.image.fromstring(drone.image, (W, H), 'RGB')
                # battery status
                hud_color = (255, 0, 0) if drone.navdata.get('drone_state', dict()).get('emergency_mask', 1) else (10, 10, 255)
                bat = drone.navdata.get(0, dict()).get('battery', 0)
                f = pygame.font.Font(None, 20)
                hud = f.render('Battery: %i%%' % bat, True, hud_color)
                screen.blit(surface, (0, 0))
                screen.blit(hud, (10, 10))
            except:
                pass

            pygame.display.flip()
            clock.tick(50)
            pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
            
            myfont = pygame.font.SysFont("monospace", 15)
            label0 = myfont.render("RETURN       Takeoff", 1, (255,255,255))
            label1 = myfont.render("SPACE        Land", 1, (255,255,255))
            label2 = myfont.render("W            Move Forward", 1, (255,255,255))
            label3 = myfont.render("S            Move Backward", 1, (255,255,255))
            label4 = myfont.render("A            Move Left", 1, (255,255,255))
            label5 = myfont.render("D            Move Right", 1, (255,255,255))
            label6 = myfont.render("UP           Move Up", 1, (255,255,255))
            label7 = myfont.render("DOWN         Move Down", 1, (255,255,255))
            label8 = myfont.render("LEFT         Turn Left", 1, (255,255,255))
            label9 = myfont.render("RIGHT        Turn Right", 1, (255,255,255))
            screen.blit(label0, (20, 10))
            screen.blit(label1, (20, 30))
            screen.blit(label2, (20, 50))
            screen.blit(label3, (20, 70))
            screen.blit(label4, (20, 90))
            screen.blit(label5, (20, 110))
            screen.blit(label6, (20, 130))
            screen.blit(label7, (20, 150))
            screen.blit(label8, (20, 170))
            screen.blit(label9, (20, 190))

        print colored("[+] ", "green") + "Shutting down...",
         
        drone.halt()
        self.reset()
        pygame.quit()
        print "Ok."
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


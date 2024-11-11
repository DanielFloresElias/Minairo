from Minairo.Minairo_TCP import *
from time import sleep

if __name__=="__main__":
    IP = '192.168.1.1'
    port = 22
    Robot = MinairoSocket(IP,port)
    Robot.run()
    Robot.confGPIO(0,'INPUT')
    while Robot.getGPIO(0):
        Robot.setW(0.2)

    Robot.stop()


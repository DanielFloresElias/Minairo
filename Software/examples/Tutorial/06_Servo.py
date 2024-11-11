from Minairo.Minairo_TCP import *
from time import sleep

if __name__=="__main__":
    IP = '192.168.1.1'
    port = 22
    Robot = MinairoSocket(IP,port)
    Robot.run()
    for i in range(0,4):
        Robot.setSERVO(0,1600)
        sleep(0.5)
        Robot.setSERVO(0,1400)
        sleep(0.5)
    Robot.stop()

